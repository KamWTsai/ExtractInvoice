import pdfplumber
import re
import pandas as pd
import shutil
import os
import argparse

parser = argparse.ArgumentParser(description="功能：截取发票金额")
parser.add_argument("-i", "--input_path", help="输入路径", default="")
parser.add_argument("-o", "--output_path", help="输出路径", default='./')
args = parser.parse_args()


class Invoice:
    def __init__(self, invoice_code, invoice_number, issue_date, buyer_name, buyer_tax_code, seller_name,
                 seller_tax_code, amount):
        self.invoice_code = invoice_code
        self.invoice_number = invoice_number
        self.issue_date = issue_date
        self.buyer_name = buyer_name
        self.buyer_tax_code = buyer_tax_code
        self.seller_name = seller_name
        self.seller_tax_code = seller_tax_code
        self.amount = amount


class InvoiceList:
    def __init__(self, invoice_list=[]):
        self.list = []
        self.list.extend(invoice_list)

    def getSumAmount(self):
        sum = 0
        for invoice in self.list:
            sum += invoice["amount"]
        return sum


# 对传入的单个PDF文件进行提取
def extractInvoice(pdf_file):
    # 对单个PDF文件进行解析
    invoice_list = InvoiceList()
    for page in pdf_file.pages:  # 逐页解析
        text = page.extract_text()

        invoice_code = re.search("发票代码.*?[0-9]{12}", text).group(0)
        invoice_code = re.search("[0-9]{12}", invoice_code).group(0)
        invoice_number = re.search("发票号码.*?[0-9]{8}", text).group(0)
        invoice_number = re.search("[0-9]{8}", invoice_number).group(0)
        issue_date = re.search("\d{4} *?年 *?\d{1,2} *?月 *?\d{1,2} *?日", text).group(0).replace(" ", "")

        name = re.findall("名 +?称.*?[\u4e00-\u9fa5]+", text)
        buyer_name = re.split("[:：]", name[0])[-1].strip()
        seller_name = re.split("[:：]", name[1])[-1].strip()

        tax_code = re.findall("纳税人识别号.*?[A-Za-z0-9]+", text)
        buyer_tax_code = re.split("[:：]", tax_code[0])[-1].strip()
        seller_tax_code = re.split("[:：]", tax_code[1])[-1].strip()

        amount = re.search("小写.*?[0-9]+.[0-9]{2}", text).group(0)
        amount = float(re.search("[0-9]+.[0-9]{2}", amount).group(0))

        invoice = Invoice(invoice_code, invoice_number, issue_date, buyer_name, buyer_tax_code, seller_name,
                          seller_tax_code, amount)

        # print(invoice.__dict__)
        invoice_list.list.append(invoice.__dict__)
    return invoice_list


# 复制并且重命名文件
def copyAndRenameFile(invoice_list, file, file_path, output_path):
    sum = invoice_list.getSumAmount()
    sum1 = format(float(sum), ".2f")
    sum2 = format(float(sum1), ",")
    decimal_places = len(sum2.split(".")[-1])
    sum = sum2 + "0" if decimal_places == 1 else sum2
    shutil.copy(file_path, output_path + "".join(file.split(".")[:-1]) + "-" + sum + "." + file.split(".")[-1])


# 写入csv文件
def writeToCsv(df, output_path):
    df.to_csv(output_path + "Invoice.csv", header=True, encoding="utf_8_sig")


def main():
    # input_path = args.input_path
    input_path = args.input_path
    output_path = args.output_path

    file_list = []

    for file in os.listdir(input_path):
        file_path = os.path.join(input_path, file)
        pdf_file = pdfplumber.open(file_path)
        invoice_list = extractInvoice(pdf_file)

        for i in invoice_list.list:
            print(i)

        file_list.extend(invoice_list.list)
        copyAndRenameFile(invoice_list, file, file_path, output_path)

    df = pd.DataFrame(file_list)
    writeToCsv(df, output_path)


if __name__ == '__main__':
    main()