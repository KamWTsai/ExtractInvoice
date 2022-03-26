# Python提取发票PDF文件中的信息

[TOC]

## 1. 需求背景

现有较多发票以PDF文件的形式存在，需要：

- 将单个PDF文件`xxx.pdf`内的几张发票的金额加总，将该PDF文件重命名为`xxx-总金额.pdf`将所有发票的信息输出到Excel中

## 2. 实现功能

1. 可读取输入路径下的所有PDF，并且将识别后的文件复制到输出路径并重命名
2. 将所有发票的信息输出到Excel中，方便后续使用

## 3. 准备工作

安装Python第三方库：pdfplumber、pandas

```
pip install pdfplumber
pip install pandas
```

- pdfplumber：用于解析PDF文件中的信息，并且提取出来
- pandas：此处用于将多个发票的信息输出到csv

## 4. 运行

1. 在`ExtractInvoice.py`所在路径打开`cmd`（也可以先打开cmd，然后cd到py文件所在路径）

2. 输入命令：

   ```
   python ExtractInvoice.py -i 输入路径 -o 输出路径
   ```

   - -i：后面跟输入路径。输入路径为文件夹
   - -o：后面跟输出路径。输出路径为文件夹
   - 请注意输入路径下请保证<u>均为发票pdf文件</u>，否则会报错（后期计划增加识别是否为pdf文件，否则抛出异常）

## 5. 代码核心逻辑

- 类：

  1. Invoice：发票类，单张发票为1个对象。属性为发票代码、发票号码、开票时间、购买方名称、购买方纳税人识别号、销售方名称、销售方纳税人识别号、金额
  2. InvoiceList：发票列表类，单个发票PDF文件为1个对象。属性list包含多个发票的信息（list内的元素不是Invoice对象，而是Invoice对象的`__dict__`信息）。方法getSumAmount()用于加总单个PDF文件的所有发票金额

- 方法extractInvoice(pdf_file)：

  1. 对传入的单个PDF文件，遍历PDF的每一页，单页为单张发票

  2. 对于单页，将PDF转文字，再用正则表达式来匹配指定的信息，生成一个Invoice对象

  3. 将Invoice对象转为dict类型（`Invoice.__dict__`），添加到InvoiceList中

## 6. 待优化

测试用例过少，发票PDF可能不够规范，可能会出现正则表达式匹配失误，识别结果需检查