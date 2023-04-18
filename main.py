# Exemplo que puxa terrenos maiores de 50.000 m2 da api Vivareal do munícipio de Presidente Prudente - SP


import pandas as pd
import requests

headers = {
    'cookie': '__cfruid=1e2802b90a93e1bffeabc9fdc794a6e659431616-1659973517',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Language"':'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'x-domain':'www.vivareal.com.br',
    'Origin':'https://www.vivareal.com.br',
    'Connection':'keep-alive',
    'Referer':'https://www.vivareal.com.br/',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'cross-site',
    'Sec-GPC':'1'
}

titles = []
descricoes = []
areas = []
operacao = []
precocompra = []
precoaluguel = []
endereco = []
cities = []
states = []
zips = []
neighs = []
links = []
lats = []
longs =[]
fa = []
p = []
count = 1


link = "https://glue-api.vivareal.com/v2/listings?addressCity=Presidente Prudente&addressLocationId=BR>Sao Paulo>NULL>Presidente Prudente&addressNeighborhood=&addressState=São Paulo&addressCountry=Brasil&addressStreet=&addressZone=&addressPointLat=-22.120594&addressPointLon=-51.387408&usableAreasMin=45000&business=SALE&facets=amenities&unitTypes=ALLOTMENT_LAND&unitSubTypes=UnitSubType_NONE,CONDOMINIUM,VILLAGE_HOUSE&unitTypesV3=RESIDENTIAL_ALLOTMENT_LAND&usageTypes=RESIDENTIAL&listingType=USED&parentId=null&categoryPage=RESULT&includeFields=search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount),page,seasonalCampaigns,fullUriFragments,nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier,phones),facets,developments(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount))&size=36&from=&q=&developmentsSize=5&__vt=&levels=CITY,UNIT_TYPE&ref=&pointRadius=&isPOIQuery="
file_name = "presidenteprudente.xlsx"
r = requests.get(link, headers=headers)
dados = r.json()

for i in dados["search"]["result"]["listings"]:
    titles.append(i['listing']['title'])
    descricoes.append(i['listing']['description'])
    aint = i['listing']['usableAreas'][0]
    areas.append(aint)


    if(len(i['listing']['pricingInfos'])>1):
        operacao.append('COMPRA/ALUGUEL')
        if(i['listing']['pricingInfos'][0]['businessType']=='RENTAL'):
            precoaluguel.append(i['listing']['pricingInfos'][0]['price'])
            precocompra.append(i['listing']['pricingInfos'][1]['price'])
        if(i['listing']['pricingInfos'][1]['businessType']=='RENTAL'):
            precoaluguel.append(i['listing']['pricingInfos'][1]['price'])
            precocompra.append(i['listing']['pricingInfos'][0]['price'])
    else:
        operacao.append('COMPRA')
        precoaluguel.append('-')
        precocompra.append(i['listing']['pricingInfos'][0]['price'])
       
    try:
        endereco.append(i['listing']['address']['street'] + ', ' + i['listing']['address']['streetNumber'])
    except:
        try:
            endereco.append(i['listing']['address']['street'])
        except:
            endereco.append('-')

    cities.append(i['listing']['address']['city'])
    states.append(i['listing']['address']['stateAcronym'])
    zips.append(i['listing']['address']['zipCode'])
    neighs.append(i['link']['data']['neighborhood'])
    links.append('https://www.vivareal.com.br/'+ i['link']['href'])
    try:
        lats.append(i['listing']['address']['point']['lat'])
    except:
        lats.append('-')
    try:
        longs.append(i['listing']['address']['point']['lon'])
    except:
            longs.append('-')


lista = list(zip(titles, descricoes, areas, operacao, precocompra, precoaluguel, endereco, cities, states, zips, neighs, links, lats, longs))

df = pd.DataFrame(lista, columns=['title', 'descricao', 'metragem', 'operacao', 'preço compra', 'preço aluguel', 'endereco', 'cidade','estado', 'cep', 'bairro', 'link', 'latitude', 'longitude'])


df.to_excel(file_name)



