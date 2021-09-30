# Geospatial-Programming-Project
References:

https://search.asf.alaska.edu/#/?zoom=6.354&center=175.730,-40.176&resultsLoaded=true&granule=ALPSRS279162650-L1.5&dataset=ALOS

https://gadm.org/download_country_v3.html

https://data.linz.govt.nz/layer/101290-nz-building-outlines/

https://data.linz.govt.nz/layer/101292-nz-building-outlines-all-sources/

I.Generate Slope

  slope=processing.run("native:slope",{parameters})

II.Create Network:

  0. Simplify WDN to simple polyline instead of multiString
  1. create end start of each polyline
  2. remove duplicated geometries to obtain junktions
  3. loop over WDN, add fields start_id end_id, create field id,x,y for each junction point.
  4. fill start_id end_id with the id of convenient Junktion

III. Junctions with Altitude and Slope

  processing.run("native:rastersampling",{parameters})

-------------------------->>>>
Paste WDNAnalysis in:
C:\Program Files\QGIS 3.20.1\apps\qgis\python\plugins
