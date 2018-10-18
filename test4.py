#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"


import json,redis
REDIS_HOST = "10.2.2.87"
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_PASSWORD = "xinnet123"

class Find_Redis(object):
    def __init__(self):

        try:
            self.POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)
            self.p = redis.Redis(connection_pool=self.POOL)

        except Exception as e:
            print("redis连接失败")
            print(e)

    def inserkeymanranking(self,keyman,key_json):

        try:
            self.p.delete("keyman:" + keyman)
            num = self.p.sadd("keyman:"+keyman,key_json)
            if num==1:
                print("添加成功")
        except Exception:
            print("插入失败")



    def getkeymanranking(self,keyman):
        result = self.p.smembers("keyman:"+keyman)
        print(result,"dddddddddddddddddddddd")
        if not result:
            print(111)
            return None
        else:
            print(222)
            # print(list(result)[0])
            result_dict = list(result)[0]
            print(result_dict)
            # return result_dict
cc = {'keyman': '商标', 'index': {'quanwang': '317,146', 'baiduPc': '1293', 'baiduMove': '1179', '360index': '5708', 'sougouPc': '122,231', 'weixin': '138,348', 'shougouMove': '48,286', 'total': '32,700,000', 'top_domain': 9, 'context_page': 11}, 'ranking': [{'domainName': 'sbj.saic.gov.cn', 'description': '国家工商行政管理总局商标局_中国商标网官网'}, {'domainName': 'ctmo.gov.cn', 'description': '国家工商行政管理总局商标局_中华人民共和国国家工商行政管理总局'}, {'domainName': 'wsjs.saic.gov.cn', 'description': '商标网上检索系统'}, {'domainName': 'tmkoo.com', 'description': '商标查询 - 商标注册查询 - 中国商标网 - 标库网官网'}, {'domainName': 'gbicom.cn', 'description': '商标转让-中国专业的闲置商标转让平台-中华商标超市网'}, {'domainName': 'cmsbw.cn', 'description': '商标转让_中国领先的专业商标交易平台-创名商标转让网'}, {'domainName': 'ipr.zbj.com', 'description': '商标注册|商标查询|专利申请|版权登记|代理机构-八戒知识产权[官网]'}, {'domainName': '86sb.com', 'description': '商标转让_商标转让网_商标交易平台-买商标,找尚标'}, {'domainName': 'quandashi.com', 'description': '商标查询|商标注册|专利查询|专利申请|版权登记-权大师官网'}], 'top10': [{'domainName': ParseResult(scheme='', netloc='', path='sbj.saic.gov.cn', params='', query='', fragment=''), 'description': '国家工商行政管理总局商标局_中国商标网官网', 'domainUrl': 'http://sbj.saic.gov.cn/'}, {'domainName': ParseResult(scheme='', netloc='', path='sbj.saic.gov.cn/sbcx', params='', query='', fragment=''), 'description': '商标查询_中国商标网', 'domainUrl': 'http://sbj.saic.gov.cn/sbcx/'}, {'domainName': ParseResult(scheme='', netloc='', path='baike.baidu.com/link', params='', query='url=NKb7hMiQ2TaK6BkUVl0ac_qmU8mwoKvtF_ZdrpotLcxg7axTZRxKOjoGprPsuiSBIobzNHSUKs_JRSCubFxab8jJM5GMj6fYUnF8sqAcgHO', fragment=''), 'description': '商标_百度百科', 'domainUrl': 'http://baike.baidu.com/link?url=NKb7hMiQ2TaK6BkUVl0ac_qmU8mwoKvtF_ZdrpotLcxg7axTZRxKOjoGprPsuiSBIobzNHSUKs_JRSCubFxab8jJM5GMj6fYUnF8sqAcgHO'}, {'domainName': ParseResult(scheme='', netloc='', path='ctmo.gov.cn', params='', query='', fragment=''), 'description': '国家工商行政管理总局商标局_中华人民共和国国家工商行政管理总局', 'domainUrl': 'http://www.ctmo.gov.cn/'}, {'domainName': ParseResult(scheme='', netloc='', path='wsjs.saic.gov.cn', params='', query='', fragment=''), 'description': '商标网上检索系统', 'domainUrl': 'http://wsjs.saic.gov.cn/'}, {'domainName': ParseResult(scheme='', netloc='', path='baike.baidu.com/item/%E5%95%86%E6%A0%87%E5%88%86%E7%B1%BB%E8%A1%A8/9204053', params='', query='', fragment=''), 'description': '商标分类表_百度百科', 'domainUrl': 'https://baike.baidu.com/item/%E5%95%86%E6%A0%87%E5%88%86%E7%B1%BB%E8%A1%A8/9204053'}, {'domainName': ParseResult(scheme='', netloc='', path='tmkoo.com', params='', query='', fragment=''), 'description': '商标查询 - 商标注册查询 - 中国商标网 - 标库网官网', 'domainUrl': 'http://www.tmkoo.com/'}, {'domainName': ParseResult(scheme='', netloc='', path='baike.baidu.com/item/r%E5%95%86%E6%A0%87/6968535', params='', query='', fragment=''), 'description': 'r商标_百度百科', 'domainUrl': 'https://baike.baidu.com/item/r%E5%95%86%E6%A0%87/6968535'}, {'domainName': ParseResult(scheme='', netloc='', path='gbicom.cn', params='', query='', fragment=''), 'description': '商标转让-中国专业的闲置商标转让平台-中华商标超市网', 'domainUrl': 'http://www.gbicom.cn/'}, {'domainName': ParseResult(scheme='', netloc='', path='hanyu.baidu.com/zici/s', params='', query='wd=%E5%95%86%E6%A0%87&query=%E5%95%86%E6%A0%87&srcid=28232&from=kg0&from=kg0', fragment=''), 'description': '商标_百度汉语', 'domainUrl': 'https://hanyu.baidu.com/zici/s?wd=%E5%95%86%E6%A0%87&query=%E5%95%86%E6%A0%87&srcid=28232&from=kg0&from=kg0'}], 'baike': '商标(trade mark) 是一个专门的法律术语。品牌或品牌的一部分在政府有关部门依法注册后，称为“商标”。商标受法律的保护，注册者有专用权。国际市场上著名的商标，往往在许多国家注册。中国有“注册商标”与“未注册商标”之区别。注册商标是在政府有关部门注册后受法律保护的商标，未注册商标则不受商标法律的保护。img[1-2]'}






if __name__ =="__main__":
    rd = Find_Redis()
    aa = rd.getkeymanranking("商标")
    print(aa)



c= {'entLogo': '/static/pc/photo/logo.png', 'shareLogo': 'https://ts.bdimg.com/biz/ecom/vmp/zx_ent_logo_default@2x.png', 'entName': '汤阴县新网资产管理有限公司', 'bdCode': 301813064913, 'openStatus': '开业', 'entType': '有限责任公司(自然人投资或控股的法人独资)', 'isClaim': 4, 'claimUrl': '-', 'benchMark': True, 'regNo': '91410523687116404F', 'orgNo': '68711640-4', 'taxNo': '-', 'scope': '房屋、厂地、机械设备租赁、资产管理', 'regAddr': '汤阴县城关精忠路', 'legalPerson': '于爱军', 'startDate': '2009-03-26', 'openTime': '2009-03-26至2023-03-25', 'annualDate': '2017-05-25', 'regCapital': '300万(元)', 'industry': '-', 'telephone': '138****9813', 'district': '河南省安阳市汤阴县', 'authority': '安阳市汤阴县工商行政管理局', 'realCapital': '-', 'orgType': '-', 'scale': '-', 'directors': [{'name': '于爱军', 'gender': '-', 'title': '执行董事兼总经理', 'img': '/static/pc/photo/directors.png'}, {'name': '李岩', 'gender': '-', 'title': '监事', 'img': '/static/pc/photo/directors.png'}], 'shares': [{'name': '汤阴县供销合作社', 'type': '事业法人', 'img': '/static/pc/photo/shares.png', 'amount': '300万(元)'}], 'districtCode': '1004:410523'}


qq = {"status":0,"msg":"","data":{"entLogo":"/static/pc/photo/logo.png","shareLogo":"https://ts.bdimg.com/biz/ecom/vmp/zx_ent_logo_default@2x.png","entName":"u4e00u9e23u65f6u4ee3uff08u5317u4eacuff09u4f20u5a92u5e7fu544au6709u9650u516cu53f8u6cf0u5ddeu5206u516cu53f8","bdCode":431216860126,"openStatus":"u6ce8u9500","entType":"u6709u9650u8d23u4efbu516cu53f8u5206u516cu53f8(u81eau7136u4ebau6295u8d44u6216u63a7u80a1)","isClaim":4,"claimUrl":"-","benchMark":"","regNo":"321284000095928","orgNo":"-","taxNo":"-","scope":";u65e0u3002;u5e7fu544au8bbeu8ba1u3001u5236u4f5cu3001u4ee3u7406u3001u53d1u5e03uff1bu5e7fu544au4fe1u606fu54a8u8be2u3002","regAddr":"u59dcu5830u5e02u59dcu5830u9547u8a79u56ed7u53f7u697c05u5ba4u8425u4e1au623f","legalPerson":"u738bu6842u51e4","startDate":"2010-06-02","openTime":"u957fu671fu6709u6548","annualDate":"2014-11-05","regCapital":"-","industry":"-","telephone":"-","district":"u6c5fu82cfu7701u6cf0u5ddeu5e02u59dcu5830u5e02","authority":"u6cf0u5ddeu5e02u59dcu5830u5de5u5546u884cu653fu7ba1u7406u5c40","realCapital":"-","orgType":"-","scale":"-","directors":[],"shares":[],"districtCode":"1004:321284","revokeDate":"2014-11-05"}}


ccc = {'entLogo': '/static/pc/photo/logo.png', 'shareLogo': 'https://ts.bdimg.com/biz/ecom/vmp/zx_ent_logo_default@2x.png', 'entName': 'u4e00u9e23u65f6u4ee3uff08u5317u4eacuff09u4f20u5a92u5e7fu544au6709u9650u516cu53f8u6cf0u5ddeu5206u516cu53f8', 'bdCode': 431216860126, 'openStatus': 'u6ce8u9500', 'entType': 'u6709u9650u8d23u4efbu516cu53f8u5206u516cu53f8(u81eau7136u4ebau6295u8d44u6216u63a7u80a1)', 'isClaim': 4, 'claimUrl': '-', 'benchMark': '', 'regNo': '321284000095928', 'orgNo': '-', 'taxNo': '-', 'scope': ';u65e0u3002;u5e7fu544au8bbeu8ba1u3001u5236u4f5cu3001u4ee3u7406u3001u53d1u5e03uff1bu5e7fu544au4fe1u606fu54a8u8be2u3002', 'regAddr': 'u59dcu5830u5e02u59dcu5830u9547u8a79u56ed7u53f7u697c05u5ba4u8425u4e1au623f', 'legalPerson': 'u738bu6842u51e4', 'startDate': '2010-06-02', 'openTime': 'u957fu671fu6709u6548', 'annualDate': '2014-11-05', 'regCapital': '-', 'industry': '-', 'telephone': '-', 'district': 'u6c5fu82cfu7701u6cf0u5ddeu5e02u59dcu5830u5e02', 'authority': 'u6cf0u5ddeu5e02u59dcu5830u5de5u5546u884cu653fu7ba1u7406u5c40', 'realCapital': '-', 'orgType': '-', 'scale': '-', 'directors': [], 'shares': [], 'districtCode': '1004:321284', 'revokeDate': '2014-11-05'}


v = {"status":0,"msg":"","data":{"entLogo":"\/static\/pc\/photo\/logo.png","shareLogo":"https:\/\/ts.bdimg.com\/biz\/ecom\/vmp\/zx_ent_logo_default@2x.png","entName":"\u6c5f\u82cf\u95ea\u5b9c\u8d2d\u7535\u5b50\u5546\u52a1\u6709\u9650\u516c\u53f8","bdCode":238896022146,"openStatus":"\u5f00\u4e1a","entType":"\u6709\u9650\u8d23\u4efb\u516c\u53f8(\u81ea\u7136\u4eba\u6295\u8d44\u6216\u63a7\u80a1)","isClaim":4,"claimUrl":"-","benchMark":"","regNo":"91320903071041301Q","orgNo":"07104130-1","taxNo":"320903071041301","scope":"\u5728\u4e92\u8054\u7f51\u4e0a\u9500\u552e\u901a\u7528\u673a\u68b0\u8bbe\u5907\u3001\u4e94\u91d1\u4ea7\u54c1\u3001\u7535\u5b50\u4ea7\u54c1\u3001\u7535\u6c14\u8bbe\u5907\u3001\u5bb6\u7528\u7535\u5668\u3001\u706f\u5177\u3001\u88c5\u9970\u7269\u54c1\u3001\u53a8\u623f\u536b\u751f\u95f4\u7528\u54c1\u53ca\u65e5\u7528\u6742\u54c1\u3001\u6d82\u6599\uff1b\u4f1a\u8bae\u53ca\u5c55\u89c8\u670d\u52a1\uff0c\u9152\u5e97\u7ba1\u7406\u670d\u52a1\uff0c\u65c5\u6e38\u54a8\u8be2\u670d\u52a1\uff0c\u623f\u5c4b\u79df\u8d41\uff0c\u7269\u4e1a\u7ba1\u7406\u670d\u52a1\u3002\uff08\u4f9d\u6cd5\u987b\u7ecf\u6279\u51c6\u7684\u9879\u76ee\uff0c\u7ecf\u76f8\u5173\u90e8\u95e8\u6279\u51c6\u540e\u65b9\u53ef\u5f00\u5c55\u7ecf\u8425\u6d3b\u52a8\uff09","regAddr":"\u76d0\u57ce\u76d0\u90fd\u533a\u5188\u4e2d\u8857\u9053\u6c11\u6842\u8def1\u53f7(T)","legalPerson":"\u845b\u6210\u5947","startDate":"2013-06-17","openTime":"2013-06-17 \u81f3 2033-06-16","annualDate":"2016-05-05","regCapital":"1,000\u4e07(\u5143)","industry":"-","telephone":"0515-8843****","district":"\u6c5f\u82cf\u7701\u76d0\u57ce\u5e02\u76d0\u90fd\u533a","authority":"\u76d0\u57ce\u5e02\u5de5\u5546\u884c\u653f\u7ba1\u7406\u5c40","realCapital":"-","orgType":"-","scale":"-","directors":[],"shares":[],"districtCode":"1004:320903"}}


f = {"status":0,"msg":"","data":{"entLogo":"\/static\/pc\/photo\/logo.png","shareLogo":"https:\/\/ts.bdimg.com\/biz\/ecom\/vmp\/zx_ent_logo_default@2x.png","entName":"\u4f5b\u5c71\u5e02\u5357\u6d77\u533a\u6842\u57ce\u5e78\u4f0d\u7cae\u6cb9\u96f6\u552e\u90e8","bdCode":171742902912,"openStatus":"\u6ce8\u9500","entType":"\u4e2a\u4f53\u5de5\u5546\u6237","isClaim":4,"claimUrl":"-","benchMark":{"regcapital":{"province":null,"country":null}},"regNo":"440682600977624","orgNo":"-","taxNo":"-","scope":"-","regAddr":"\u4e0a\u6d77\u5e02\u5609\u5b9a\u533a\u771f\u65b0\u8857\u9053\u4e07\u9547\u8def599\u53f72\u5e621\u5c42118\u5ba4","legalPerson":"\u5e78\u5176\u660c","startDate":"2003-07-01","openTime":"2003-07-01 \u81f3 \u65e0\u56fa\u5b9a\u671f\u9650","annualDate":"2005-04-13","regCapital":"10\u4e07(\u5143)","industry":"-","telephone":"8855****","district":"\u5e7f\u4e1c\u7701\u4f5b\u5c71\u5e02\u5357\u6d77\u5e02","authority":"\u4f5b\u5c71\u5e02\u5357\u6d77\u533a\u5de5\u5546\u884c\u653f\u7ba1\u7406\u5c40","realCapital":"-","orgType":"-","scale":"-","directors":[],"shares":[],"districtCode":"1004:330104","childTabData":{"investRelation":{"invest":0,"branch":0},"risk":{"discredited":0,"abnormal":0,"law":0,"quality":0,"food":0,"penalty":0}}}}