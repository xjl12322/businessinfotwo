#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

def insert(item):

    print("--------------------------")
    print(item["company_introduce"], "1111111111111")
    print(item["tel"], "22222222222")
    print(item["contacts_people"], "33333333333")
    print(item["m_phone"], "44444444444")
    print(item["company_name"], "5555555555")
    print(item["status"], "66666666666")
    print(item["company_type"], "77777777")
    print(item["establish_date"], "888888888888")
    print(item["expire_date"], "9999999999")
    print(item["register_money"], "aaaaaaaaaa")
    print(item["register_authority"], "bbbbbbbbbb")
    print(item["business_scope"], "ccccccccccccc")
    print(item["register_address"], "dddddddddddd")
    print(item["legal_representative"], "eeeeeeeeee")
    print(item["register_num"])
    print(item["company_website"])
    print(item["industry_id"])
    print(item["area_p"], "nnnnnnnnnn")
    print(item["area_s"], "ppppppppp")
    print(item["area_q"], "ooooooo")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    eid = mad5_url(item["company_name"])

    print(eid, "eideideideideideideideid")
    sql2 = "insert ignore into business(eid,company_introduce,tel,contacts_people,m_phone,company_name,status,company_type,establish_date,expire_date,register_money,register_authority,business_scope,register_address,legal_representative,register_num,company_website,industry_id,area_p,area_s,area_q,origin_id,industry) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    num_businessinfoitem = cursor.execute(sql2, (
    eid, item["company_introduce"], item["tel"], item["contacts_people"], item["m_phone"], item["company_name"],
    item["status"], item["company_type"], str(item["establish_date"]), item["expire_date"], item["register_money"],
    item["register_authority"], item["business_scope"], item["register_address"], item["legal_representative"],
    item["register_num"], item["company_website"], item["industry_id"], item["area_p"], item["area_s"], item["area_q"],
    item["origin_id"], item["industry"]))
    if num_businessinfoitem:
        cursor.execute('select last_insert_id() as id')
        id = cursor.fetchone()
        self.loging.info("insert database seccess: ID is :{}".format(id["id"]))
    else:
        self.loging.info("insert database fail,in exist")
    if item["register_address"]:
        company_c = {
            "compName": item["company_name"],
            "compAddress": item["register_address"]
        }
        try:
            b = c_company(company_c)
            self.loging.info("es状态{}".format(b))
            if (b == "true") or (b == True) or (b == "True"):
                self.loging.info("插入es成功")
            else:
                self.loging.info("插入es失败")
        except Exception as e:
            self.loging.info("异常信息".format(e))
            self.loging.info("插入es异常")