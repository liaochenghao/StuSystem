### 获取支付方式

**请求地址**:
```
    GET     /common/order_currency_payment/
```

**请求参数**:
```
    无
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
            "key": "DOLLAR",
            "verbose": "美金",
            "payment": [
                {
                    "key": "BANK",
                    "verbose": "银行转账",
                    "payment_information": [
                        {
                            "payment": "BANK",
                            "currency": "FOREIGN_CURRENCY",
                            "account_number": "scc@iauss.org",
                            "account_name": "International Association of University Summer Sessions"
                        }
                    ]
                },
                {
                    "key": "PAY_PAL",
                    "verbose": "PAY_PAL转账",
                    "payment_information": [
                        {
                            "payment": "PAY_PAL",
                            "bank_name": "Bank of America",
                            "opening_bank": "1761 Massachusetts Ave, LexingtonMA 02420",
                            "currency": "FOREIGN_CURRENCY",
                            "account_name": "International Association of University Summer Sessions",
                            "swift_code": "BOFAUS3N",
                            "routing_number_paper": "011000138",
                            "swift_code_foreign_currency": "BOFAUS6S",
                            "company_address": "12 Dunham Street, Lexington, MA 02420",
                            "account_number": "4666190664",
                            "routing_number_wires": "026009593"
                        }
                    ]
                }
            ]
        },
        {
            "key": "RMB",
            "verbose": "人民币",
            "payment": [
                {
                    "key": "BANK",
                    "verbose": "银行转账",
                    "payment_information": [
                        {
                            "payment": "BANK",
                            "currency": "RMB",
                            "account_number": "3202018609200099381",
                            "account_name": "贝壳联投(武汉)科技有限公司",
                            "opening_bank": "中国工商银行股份有限公司武汉邮科院支行"
                        }
                    ]
                },
                {
                    "key": "ALI_PAY",
                    "verbose": "支付宝转账",
                    "payment_information": [
                        {
                            "payment": "ALI_PAY",
                            "currency": "RMB",
                            "account_number": "scc@iauss.org",
                            "account_name": "贝壳联投(武汉科技有限公司)"
                        }
                    ]
                }
            ]
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```