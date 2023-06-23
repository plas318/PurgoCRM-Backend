import os
import xml.etree.ElementTree as et

import requests
from datetime import datetime


key = os.getenv('HospitalKey')


# names like functions, variables are not organized.
# some exceptions may be omitted.
# the api returning hospinfo is just for tests. not complete.


def get_hospinfo_openapi(): 
    hospinfo_openapi = {}

    for pageno in range(1, 9):
        try:
            r = requests.get(
                'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList?' \
                '&numOfRows=10000' \
                '&ServiceKey=%s' \
                '&pageNo=%s'
                %(key, str(pageno))
                )
        except Exception as e:
            print(e)
            raise Exception('An openapi request error occured.')

        try: #
            root = et.fromstring(r.text)
            items = root[1][0]
        except Exception as e:
            print(e)
            raise Exception('A XML parsing error occured.')

        for item in items:
            if not (class_code_name:=item.find('clCd')).text in ['01', '11', '41', '51']: 
                continue

            hospital_id = hospital_id.text if (hospital_id:=item.find('ykiho')) != None else None
            hospital_name = hospital_name.text if (hospital_name:=item.find('yadmNm')) != None else None
            class_code = class_code.text if (class_code:=item.find('clCdNm')) != None else None
            class_code_name = int(class_code_name.text) if (class_code_name:=item.find('clCd')) != None else None
            phone = phone.text if (phone:=item.find('telno')) != None else None
            url = url.text if (url:=item.find('hospUrl')) != None else None
            established_at = datetime.strptime(established_at.text, '%Y%m%d').date() if (established_at:=item.find('estbDd')) != None else None 
            # datetime.strptime(established_at.text, '%Y%m%d').date()
            sggu_name = sggu_name.text if (sggu_name:=item.find('sgguCdNm')) != None else None
            emdong_name = emdong_name.text if (emdong_name:=item.find('emdongNm')) != None else None
            post_no = int(post_no.text) if (post_no:=item.find('postNo')) != None else None
            address = address.text if (address:=item.find('addr')) != None else None
            sido_name = sido_name.text if (sido_name:=item.find('sidoCdNm')) != None else None
            sggu_no = int(sggu_no.text) if (sggu_no:=item.find('sgguCd')) != None else None
            sido_no = int(sido_no.text) if (sido_no:=item.find('sidoCd')) != None else None
            general_doctor_count = int(general_doctor_count.text) if (general_doctor_count:=item.find('detyGdrCnt')) != None else None
            intern_count = int(intern_count.text) if (intern_count:=item.find('detyIntnCnt')) != None else None
            resident_count = int(resident_count.text) if (resident_count:=item.find('detyResdntCnt')) != None else None
            fellow_doctor_count = int(fellow_doctor_count.text) if (fellow_doctor_count:=item.find('detySdrCnt')) != None else None

            hospinfo_openapi[hospital_id] = {
                'hospital_name': hospital_name,
                'class_code': class_code,
                'class_code_name': class_code_name,
                'phone': phone,
                'url': url,
                'established_at': established_at,
                'sggu_name': sggu_name,
                'emdong_name': emdong_name,
                'post_no': post_no,
                'address': address,
                'sido_name': sido_name,
                'sggu_no': sggu_no,
                'sido_no': sido_no,
                'general_doctor_count': general_doctor_count,
                'intern_count': intern_count,
                'resident_count': resident_count,
                'fellow_doctor_count': fellow_doctor_count
                }

    return hospinfo_openapi

