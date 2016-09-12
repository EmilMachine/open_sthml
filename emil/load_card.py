from owslib.wms import WebMapService

### sources
# http://dataportalen.stockholm.se/dataportalen/
# Title: Stockholmskartan
#
# 


### BASIC DOC
#print(wms.identification.type)
#print(wms.identification.title)
#print(list(wms.contents))

# wms = WebMapService('http://openmap.stockholm.se/bios/wms/app/baggis/web/WMS_STHLM_STOCKHOLMSKARTA_GRA_FORENKLAD')
##> 'Stockholmskarta gra_forenklad Stockholms stad'
##> ['stockholmskarta_gra_forenklad', u's_h\xf6jder_rh2000', u't_anl\xe4ggningar', u's_gr\xe4nser_illustration', u't_gr\xe4nser_illustration', 's_byggnader_text', 's_koloni', u's_best\xe4mmelser', u's_hamnanl\xe4ggningar', u's_idrottsanl\xe4ggningar', u's_teknikanl\xe4ggningar', u's_markanl\xe4ggningar', u's_trafikanl\xe4ggningar', u's_\xf6vriga_anl\xe4ggningar', 't_adress_ort_och_gata', 's_infrastruktur_utbredning', 't_infrastruktur_bytesplats', 't_byggnader_text', 't_byggnader_linje', 't_byggnader_yta', 's_administrativ_indelning_text', 's_administrativ_indelning_ytgeometri', 's_registerenhet', u's_kvalitetsomr\xe5de', u's_kartografiskt_omr\xe5de', u't_gcf\xf6rbindelse', 's_adress_ort_och_gata', 't_bebyggelse', 's_natur', 't_natur', 't_infrastruktur_knutpunkter', u's_infrastruktur_avgr\xe4nsning', 't_infrastruktur_utbredning', 's_infrastruktur_bytesplats', u's_infrastruktur_f\xf6rbindelse', u't_infrastruktur_f\xf6rbindelse', u'l_infrastruktur_f\xf6rbindelse', 's_byggnader_linje', 's_byggnader_yta', 't_administrativ_indelning_text', 't_geografiska_namn', 's_geografiska_namn', u't_h\xf6jder', 'rn_adress_ort_och_gata', 'rn_geografiska_namn', u'rn_infrastruktur_f\xf6rbindelse', 'rn_infrastruktur_utbredning', 'rn_natur', u'rn_trafikanl\xe4ggningar', 'rn_administrativ_indelning_text', 'projektgrafik']


# wms = WebMapService('http://openmap.stockholm.se/bios/wms/app/baggis/web/WMS_STHLM_STOCKHOLMSKARTA_GRA_FORENKLAD_RASTER')
##> Stocksholmskarta gra-gron forenklad raster Stockholms stad
##> ['stockholmskarta_gra_forenklad_raster']


### TRY LOADING MAP
#wms = WebMapService('http://openmap.stockholm.se/bios/wms/app/baggis/web/WMS_STHLM_STOCKHOLMSKARTA_GRA_FORENKLAD_RASTER')
# img = wms.getmap(layers=['stockholmskarta_gra_forenklad_raster']
#                 ,srs='EPSG:2179'
#                 ,bbox=(0, 0, 10, 10)
#                 ,size=(20, 20)
#                 ,format='application/pdf'
#                 )
##> KeyError: 'content-type'



# wms = WebMapService('http://openmap.stockholm.se/bios/wms/app/baggis/web/WMS_STHLM_STOCKHOLMSKARTA_GRA_FORENKLAD')
# print(wms.identification.type)
# print(wms.getOperationByName('GetMap').methods)
# print(list(wms.contents))
# print(wms['stockholmskarta_gra_forenklad'].crsOptions)
# print(wms['stockholmskarta_gra_forenklad'].styles)
# print(wms.getOperationByName('GetMap').formatOptions)

# img = wms.getmap(layers=['stockholmskarta_gra_forenklad']
#                 ,srs='EPSG:2179'
#                 ,bbox=(0, 0, 10, 10)
#                 ,size=(20, 20)
#                 ,format='image.jpg'
#                 )
##> KeyError: 'content-type'

### NEVER GOT TO THIS POINT DUE TO content-type errors
# out = open('stholm_gray.jpg', 'wb')
# out.write(img.read())
# out.close()

'''img = wms.getmap(layers=['stockholmskarta_gra_forenklad_raster'])
                 styles=['visual_bright'],
                 srs='EPSG:4326',
                 bbox=(-112, 36, -106, 41),
                 size=(300, 250),
                 format='image/jpeg',
                 transparent=True
'''


#dpwebmap
#http://openmap.stockholm.se/bios/dpwebmap/cust_sth/sbk/openmap/DPWebMap.html?zoom=3&lat=6579934.52075&lon=152321.17572&layers=FFB00000000000T

