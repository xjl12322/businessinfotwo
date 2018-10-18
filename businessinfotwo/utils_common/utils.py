#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import conf,pymysql,hashlib,requests,json,time,redis
from DBUtils.PooledDB import PooledDB



class Utils(object):

    def __init__(self):

        mysql_host=conf.DB[conf.CURRENT_CONFIG]['MYSQL_HOST']
        mysql_db=conf.DB[conf.CURRENT_CONFIG]['MYSQL_DBNAME']
        mysql_port=conf.DB[conf.CURRENT_CONFIG]['MYSQL_PORT']
        mysql_user=conf.DB[conf.CURRENT_CONFIG]['MYSQL_USER']
        mysql_passwd=conf.DB[conf.CURRENT_CONFIG]['MYSQL_PASSWD']
        self.pool = PooledDB(pymysql, 10, host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db,
                             port=mysql_port, charset='utf8', cursorclass=pymysql.cursors.SSDictCursor)
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()


    def getsecret_pythontool(self):
        innerApp = "pythontool"
        secret = "a6d903a2-dac5-4d9d-9e6b-e32caad1dafc"
        ts = str(int(time.time() * 1000))
        sign = "innerApp=" + innerApp + "&secret=" + secret + "&ts=" + ts
        singn = self.mad5_singn(sign)
        return singn, innerApp, ts


    def mad5_singn(self,sign):

        if isinstance(sign, str):
            sign = sign.encode("utf-8")
        md5_url = hashlib.md5()
        md5_url.update(sign)
        md5_url.hexdigest()
        # print(md5_url.hexdigest())
        return md5_url.hexdigest()


    def c_company(self,company):
        sign, innerApp, ts = self.getsecret_pythontool()
        response_tdk = requests.post(
            url="https://esservice.xinnet.com/rest/whois/addOrUpdateCompany?innerApp={}&ts={}&sign={}".format(innerApp,ts, sign),json=company)
        response_tdk = json.loads(response_tdk.text)
        return response_tdk["result"]


    def insertMysql(self,item,logs):

        # print("--------------------------")
        # print(item["company_introduce"], "1111111111111")
        # print(item["tel"], "22222222222")
        # print(item["contacts_people"], "33333333333")
        # print(item["m_phone"], "44444444444")
        # print(item["company_name"], "5555555555")
        # print(item["status"], "66666666666")
        # print(item["company_type"], "77777777")
        # print(item["establish_date"], "888888888888")
        # print(item["expire_date"], "9999999999")
        # print(item["register_money"], "aaaaaaaaaa")
        # print(item["register_authority"], "bbbbbbbbbb")
        # print(item["business_scope"], "ccccccccccccc")
        # print(item["register_address"], "dddddddddddd")
        # print(item["legal_representative"], "eeeeeeeeee")
        # print(item["register_num"])
        # print(item["company_website"])
        # print(item["industry_id"])
        # print(item["area_p"], "nnnnnnnnnn")
        # print(item["area_s"], "ppppppppp")
        # print(item["area_q"], "ooooooo")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        eid = self.mad5_url2(item["company_name"])
        sql = "insert ignore into business(eid,company_introduce,tel,contacts_people,m_phone,company_name,status,company_type,establish_date,expire_date,register_money,register_authority,business_scope,register_address,legal_representative,register_num,company_website,industry_id,area_p,area_s,area_q,industry) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            num_businessinfoitem = self.cursor.execute(sql,(eid,item["company_introduce"],item["tel"], item["contacts_people"], item["m_phone"],item["company_name"],item["status"], item["company_type"], str(item["establish_date"]), item["expire_date"],item["register_money"], item["register_authority"], item["business_scope"], item["register_address"],item["legal_representative"], item["register_num"], item["company_website"],item["industry_id"],item["area_p"],item["area_s"],item["area_q"],item["industry"]))
            try:
                self.conn.commit()

                if num_businessinfoitem:

                    try:

                        self.cursor.execute('select last_insert_id() as id')
                        id = self.cursor.fetchone()
                        # return num_businessinfoitem
                        logs.info("插入数据库成功：{}".format(id))
                        es_flag = self.insertEs(item)
                        if es_flag == True:
                            logs.info("插入es成功")
                        elif es_flag == False:
                            logs.info("插入es失败")
                        elif "插入es异常" in es_flag:
                            logs.info(es_flag)

                    except Exception as e:

                        # return "getidfail:{}".format(e)
                        logs.info("插入异常:{}".format(e))

                else:

                    sql2 = 'select * from business where company_name=%s'
                    sql3 = 'UPDATE business SET status = %s, company_type = %s,establish_date = %s,expire_date = %s,register_money = %s,register_authority = %s,business_scope = %s,register_address = %s,legal_representative = %s,register_num = %s,company_website = %s,industry = %s WHERE company_name=%s'
                    try:
                        self.cursor.execute(sql2, (item["company_name"],))

                    except Exception as e:
                        logs.info("查询异常:{}".format(e))
                    alls = self.cursor.fetchone()
                    # register_num_flag = alls.get("register_num", "")
                    # print(register_num_flag)
                    if alls.get("register_num", "") == "":
                        try:
                            self.cursor.execute(sql3, (
                            item["status"], item["company_type"], item["establish_date"], item["expire_date"],
                            item["register_money"], item["register_authority"], item["business_scope"],
                            item["register_address"], item["legal_representative"], item["register_num"],
                            item["company_website"], item["industry"], item["company_name"]))
                            # return num_businessinfoitem
                            self.conn.commit()
                            logs.info("更新成功:id-{}".format(alls.get("id")))

                            es_flag = self.insertEs(item)
                            if es_flag == True:
                                logs.info("插入es成功")
                            elif es_flag == False:
                                logs.info("插入es失败")
                            elif "插入es异常" in es_flag:
                                logs.info(es_flag)

                        except Exception as e:
                            self.conn.rollback()
                            logs.info("更新异常:{}".format(e))

                            # self.loging.info("insert database fail,in exist")
                    else:
                        logs.info("数据完整无需更新")
            except Exception as e:
                logs.info("插入异常:{}".format(e))
                self.conn.rollback()


        except Exception as e:

            # return "mysqlerr:{}".format(e)
            logs.info("mysqlerror:{}".format(e))






    def insertEs(self,item):
        if item["register_address"]:
            company = {
                "compName": item["company_name"],
                "compAddress": item["register_address"]
            }
            try:
                b = self.c_company(company)
                if (b == "true") or (b == True) or (b == "True"):
                    # logs.info("插入es成功")
                    return True

                else:
                    return False
                    # logs.info("插入es成功")
            except Exception as e:
                error = "插入es异常,异常信息".format(e)
                return error
                # logs.info("插入es异常,异常信息".format(e))





    def mad5_url2(self,url):
        '''mad加密功能
        parmes：对每个文章url链接md5加密相同长度的指纹
        '''
        urls = "@$^&)*%" + url
        if isinstance(urls, str):  # py3里全是uncode字符集 也就是str，md5前判断 因为py3 unicode不能直接md5必须转换utf-8，相反py2则不用
            urls = urls.encode("utf-8")
        try:
            md5_url = hashlib.md5()
            md5_url.update(urls)
            return md5_url.hexdigest()
        except Exception as e:
            print(e, "md5")
            return ""


    def connect_redis(self):
        REDIS_HOST = conf.REDIS[conf.CURRENT_CONFIG]['host']
        REDIS_PORT = conf.REDIS[conf.CURRENT_CONFIG]['port']
        REDIS_DB = conf.REDIS[conf.CURRENT_CONFIG]['db']
        REDIS_PASSWORD = conf.REDIS[conf.CURRENT_CONFIG]['password']
        try:
            POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD,decode_responses=True)
            p = redis.Redis(connection_pool=POOL)
            return p
        except Exception as e:
            print("redis连接失败")
            print(e)
    def readmysql(self):
        r = self.connect_redis()
        print("开始读取mysql")
        '新网华视北京投资有限公司'
        try:
            self.cursor.execute('SELECT * FROM beian WHERE company_type="企业"')
            row = self.cursor.fetchone()
            num = r.sadd("beian",row["company_name"])
            print(num)
            # if num == 1:
            #     print("{}写入redis成功1--{}".format(num, row["company_name"]))
            try:
                while row is not None:
                    try:
                        row = self.cursor.fetchone()
                        keyword = row["company_name"] if "有限公司" not in row["company_name"] else str(row["company_name"]).replace("有限公司","")
                        num = r.sadd("beian", keyword)
                        if num == 1:
                            print("{}写入redis成功--{}".format(num, row["company_name"]))
                        else:
                            print("{}已存在-跳过{}".format(num, row["company_name"]))
                            continue
                    except Exception as e:
                        print(e)
            except Exception as e:
                print("ssl{}".format(e))
        except Exception as e:
            print("sql{}".format(e))


        # cur.close()
        # conn.close()
if __name__ =="__main__":
    # print("1")
    u = Utils()
    u.readmysql()
    # c = u.mad5_url2("sefs")
    # print(c)