

#lOADING LAYERS AND REMOVING PREVIOUS ONES IF EXIST
QgsProject.instance().removeAllMapLayers()
dem=QgsRasterLayer('D:\OneDrive\MASTER\semester4\GeospatialProgramming\Module5\Raheem\Delivery\data\dem.tif', "dem")
wdn=QgsVectorLayer('D:\OneDrive\MASTER\semester4\GeospatialProgramming\Module5\Raheem\Delivery\data\wdn.shp', "WDN")

vald=''
#testing if layers are valid
if not dem.isValid():
        vald='DEM'
if not wdn.isValid():
        vald=vald+' WDN'
        
if len(vald)!=0:
    print('Layers are not valid')
else: 
    #Loading layers
    QgsProject.instance().addMapLayer(dem)
    QgsProject.instance().addMapLayer(wdn) 

    #1...............Create Slope Layer
    #generating the slope layer        
    processing.runAndLoadResults("native:slope", {'INPUT': dem, 'Z_FACTOR':1, 'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
    print('#1............... Slope Layer Generated succefully')        
    #2...............Build Newtwork and junkions
    
    
    #water Network layer opening       
    line_layer=wdn
    #MultiLine String to  LineString
    wdn=processing.run("native:multiparttosingleparts", {'INPUT': line_layer, 'OUTPUT': 'memory:water distribution network' })["OUTPUT"]
    #new layer of juctions
    point_layer = QgsVectorLayer("Point?crs=epsg:32760", "point_layer", 'memory')
    #Remove duplicated points
    junktions=processing.run("native:deleteduplicategeometries", {'INPUT': point_layer, 'OUTPUT': 'memory:junktions' })["OUTPUT"]   

    pr = junktions.dataProvider()
    pr1 = wdn.dataProvider()
    junktions.startEditing()
    wdn.startEditing()

    pr.addAttributes([ QgsField("id", QVariant.Int), QgsField("x", QVariant.Double), QgsField("y", QVariant.Double)])
    pr1.addAttributes([ QgsField("start_id", QVariant.Int), QgsField("end_id", QVariant.Int)])
    i=0

    wdn.commitChanges()
    wdn.startEditing()

    junktions.commitChanges()
    junktions.startEditing()

    #loop over Network polylines and creating junctions

    for feature in wdn.getFeatures():
        #create a new feature of type type junction
        feat = QgsFeature(junktions.fields())
        geom = feature.geometry().asPolyline()
        #create new  start end points :j unctions
        start_point = QgsPoint(geom[0])
        end_point = QgsPoint(geom[-1])
        
        feat.setGeometry(start_point)
        feat["id"]=i
        #retreiving the x,y coordinates of polyline start end points and a affect it to x,y columns of junction
        feat["x"]=start_point.x()
        feat["y"]=start_point.y()
        #adding end start feature
        pr.addFeatures([feat])
        #update the start_id of polyline with the id of the start junction
        feature["start_id"]=i
        wdn.updateFeature(feature)
        i+=1
        
        feat.setGeometry(end_point)
        feat["id"]=i
        feat["x"]=end_point.x()
        feat["y"]=end_point.y()
        #adding end point feature
        pr.addFeatures([feat])
        feature["end_id"]=i
        wdn.updateFeature(feature)
        i+=1
        
    junktions.commitChanges()
    wdn.commitChanges()
    #add junctions and network layers 
    QgsProject.instance().addMapLayer(junktions)
    QgsProject.instance().addMapLayer(wdn)

    
    print('#2............... Network and Junktions Created  succefully')        
    #3............... Fill Junkions with corresponding Altitudes And Slopes
    slope_layer = QgsProject.instance().mapLayersByName('Slope')[0]
    dem_layer = QgsProject.instance().mapLayersByName('dem')[0]
    junktions=QgsProject.instance().mapLayersByName('junktions')[0]
    #retreive altitude value from DEM file and affect it to junction points
    junktions_altitude=processing.run("native:rastersampling", {'INPUT': junktions,'RASTERCOPY': dem_layer,'COLUMN_PREFIX':'altitude','OUTPUT': 'TEMPORARY_OUTPUT'})["OUTPUT"]
    #retreive slope value from Slope layer and affect it to junction points
    junktions_altitude_slope=processing.run("native:rastersampling", {'INPUT': junktions_altitude,'RASTERCOPY': slope_layer,'COLUMN_PREFIX':'slope','OUTPUT': 'memory:junctions_altitude_slope'})["OUTPUT"]
        

    QgsProject.instance().addMapLayer(junktions_altitude_slope)
    print('#2............... Junctions are Filled succefully') 
        