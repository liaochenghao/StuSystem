###  设置项目课程数量及相应费用

**请求地址**:
```
    PUT  /course/project/[project_id]/project_course_fee/
```

**请求参数**:
```
{
	"project_fees": [
			{
				"course_number": 1,
				"course_fee": 1000
			},
		]
}

备注： project_fees子项中course_number, course_fee为必填字段， course_number的最大值必须等于project_fees对应list的长度。
```

**成功返回**：
```

```

**失败返回**：
```

```