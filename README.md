# S-AES算法实现

## 项目介绍
本项目是根据"信息安全导论"课程第8-9次课讲述的AES算法，使用Python语言来编程实现加、解密程序、提供UI界面进行交互、实现多重加密、工作模式等功能。

## S-AEC算法介绍
S-AES（Simplified AES）是一种简化的高级加密标准，主要用于教育和学习目的。它采用 8 位的块大小和密钥长度，通常只需要 2 轮加密。S-AES 的主要步骤包括字节代换（SubBytes）、行移位（ShiftRows）、列混合（MixColumns）、和轮密钥加（AddRoundKey）。由于其简单性，适合初学者理解对称加密算法的基本概念。

## 编程和测试要求

### 第1关：基本测试
根据S-AES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是16bit的数据和16bit的密钥，输出是16bit的密文。

### 第2关：交叉测试
考虑到是"算法标准"，所有人在编写程序的时候需要使用相同算法流程和转换单元(替换盒、列混淆矩阵等)，以保证算法和程序在异构的系统或平台上都可以正常运行。设有A和B两组位同学(选择相同的密钥K)；则A、B组同学编写的程序对明文P进行加密得到相同的密文C；或者B组同学接收到A组程序加密的密文C，使用B组程序进行解密可得到与A相同的P。

### 第3关：扩展功能
考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为2 Bytes)，对应地输出也可以是ACII字符串(很可能是乱码)。

### 第4关：多重加密
1. 双重加密将S-AES算法通过双重加密进行扩展，分组长度仍然是16 bits，但密钥长度为32 bits。
2. 中间相遇攻击假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用中间相遇攻击的方法找到正确的密钥Key(K1+K2)。
3. 三重加密将S-AES算法通过三重加密进行扩展，下面两种模式选择一种完成：(1)按照32 bits密钥Key(K1+K2)的模式进行三重加密解密，(2)使用48bits(K1+K2+K3)的模式进行三重加解密。

### 第5关：工作模式
基于S-AES算法，使用密码分组链(CBC)模式对较长的明文消息进行加密。注意初始向量(16 bits) 的生成，并需要加解密双方共享。在CBC模式下进行加密，并尝试对密文分组进行替换或修改，然后进行解密，请对比篡改密文前后的解密结果。

## 实验结果

### 第1关 基础测试
测试明文 `0000000000001111`，密钥 `1111111111110000` 进行加密解密，使用解密结果查看加密解密流程是否有误。
![image](https://github.com/user-attachments/assets/188f9433-56f8-4245-94cf-248af81781e0)

#### 加密结果
![image](https://github.com/user-attachments/assets/caeede58-fbe5-4145-92dd-9ed6d4e987b6)


#### 解密结果
![image](https://github.com/user-attachments/assets/75d42ff5-55e9-44bc-b0c4-684ec06cd1ef)


### 第2关 交叉测试
#### 其他小组加密结果


#### 本小组加密结果



### 第3关 对ASCII字符串进行加密解密
#### 加密结果
![image](https://github.com/user-attachments/assets/f10b6f5d-e532-4292-a17f-37a56ce7cb4c)


#### 解密结果
![image](https://github.com/user-attachments/assets/9ed6cc56-5fd0-4947-9cc6-2e9d14265775)



### 第4关：多重加密
1. 双重加密
代码见double.py
![image](https://github.com/user-attachments/assets/cb5cfbe9-ae63-4969-aefa-181119b373b9)
加密：
![image](https://github.com/user-attachments/assets/c109bae0-0bc7-4198-bbb5-ee13799019a4)
解密：
![image](https://github.com/user-attachments/assets/8873942b-1592-43c5-b23b-29859d6d26f3)


3. 中间相遇攻击
代码见middle_attack.py

4. 三重加密
代码见threeford.py
![image](https://github.com/user-attachments/assets/1765eb49-6968-4c96-b4fd-72ff85b5e63f)
加密：
![image](https://github.com/user-attachments/assets/7204987c-ceec-49da-a516-ca46818e79d7)
解密：
![image](https://github.com/user-attachments/assets/898403ba-1f26-4787-b90e-87a7f4d9b82a)



### 第5关：工作模式
代码实现见CBC.py  
运行结果



## 总结
本次实验主要是对S-DES算法的实现和测试，包括基本测试、交叉测试、ASCII字符串加密解密、暴力破解、封闭测试等。完成了实验的基本要求

## 开发团队
- 小组：智慧组
- 成员：杨大浩、齐浩男
- 单位：重庆大学大数据与软件学院
