

	

create view momo_tmp2 as
SELECT  ACPAAA002, ACPAAA003, Companys002, Companys003, CompanyProduct003, Companys010, ACPAAA029, CompanyIntro002, ACPAAA005, ACPAAA017, Companys007, ACPAAA015,
    (
        SELECT '' + mt_a.認證字號
        FROM momo_tmp mt_a
        WHERE mt_a.Companys003 = mt_b.Companys003
        FOR XML PATH('')
        ) AS 認證字號總和
from　momo_tmp mt_b
where Companys003 is not null




create view momo_tmp as
SELECT 
	a.ACPAAA002, a.ACPAAA003, c.Companys002, c.Companys003, cp.CompanyProduct003, c.Companys010, a.ACPAAA029, ci.CompanyIntro002, a.ACPAAA005, a.ACPAAA017, c.Companys007, a.ACPAAA015,
	case when cp.CompanyProduct005　like '%字第%號%' then 'Y'　else 'N' end '認證字號'
FROM CompanyProduct cp
left join Companys c on cp.CompanyProduct001=c.GUID
left join CompanyIntro ci on ci.CompanyIntro001=c.GUID
left join ACPAAA a on a.ACPAAA001 = c.GUID
where cp.CompanyProduct002 = 'Momo'

select * from ACPAAA where ACPAAA003 =  '台灣伊莎貝爾食品股份有限公

select 
	  Companys003 '客戶名稱', 
	  Companys010 '客戶電話1',
	  CompanyIntro002 '客戶產業',
	  Companys007 '資本額', 
	  case when 認證字號總和 like '%Y%' then 'Y' else 'N' end '認證字號',
	  count(Companys003) '產品數量'

from　momo_tmp2
where Companys002 ='' and Companys007 =''
group by Companys002, Companys003, Companys010, CompanyIntro002, Companys007, 認證字號總和

select * from Companys where Companys003 =' 勇信貿易股份有限公司'