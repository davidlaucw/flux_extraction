#CASA script (Chun Wai Lau, David) 12.4.2019
##############################################################################initial setup###################################################################
line_name = 'CO'					#strongest line name
RRL_name = 'H30a' 					#RRL or weaker line name
line_mom0_file = 'NGC_3628_CO.image.mom0'		#moment 0 map for strongest line 
RRL_mom0_file = 'NGC_3628_H30a.lineimage.w.mom0' 	#moment 0 map for RRL or weaker line
chans_line = '160~205' 					#channels used for producing moment 0 map for strongest line
line_file ='NGC_3628_CO.image' 				#image cube file for strongest line 
RRL_file = 'NGC_3628_H30a.lineimage' 			#image cube file for RRL or weaker line
box = '200,220,320,320' 				#off-target region
region = '100,100,270,170' 				#on-target region
c='105,105,290,200' 					#extended region

############################################################creating mom0 map and spatial thesholds##############################################################
immoments(imagename=line_file,chans = chans_line, outfile = line_mom0_file) 		#make moment 0 map of strongest line
exportfits(imagename=line_mom0_file, fitsimage=line_mom0_file+'.fits',dropdeg=True) 	#convert moment 0 map to FITS file
line_sigma = imstat(imagename = line_mom0_file, box = box)['sigma'][0]			#measure the off-target noise(sigma) in strongest line mom0 map
line_peak = imstat(imagename = line_mom0_file, box = region)['max'][0]			#measure the peak of signal
psr = np.floor(line_peak/line_sigma)							#measure the peak to sigma ratio
steps = np.round(np.logspace(log10(3),log10(psr),num = 6,endpoint = False),1)		#create spatial thesholds from 3sigma to peak in logscale
#steps = np.round(np.linspace(3,psr,num = 7),1)
#steps = [1,3,6,12,24]

####################################################################################extracting flux#############################################################################
for i in steps:												#for every spatial theshold
	mask=line_mom0_file +'>='+str(i*line_sigma)							#create the mask above the spatial theshold
	logfile_line = line_name+'_'+str(i)+'sigma.txt'							#filename storing the flux of strongest line against frequency
	logfile_RRL = RRL_name+'_'+str(i)+'sigma.txt'							#filename storing the flux of RRL/weaker line against frequency
	specflux(imagename = line_file,mask = mask,box = region,logfile = logfile_line,stretch = True)	#extract the flux of strongest line using the spatial mask in the target region
	specflux(imagename = RRL_file,mask = mask,box = region, logfile = logfile_RRL,stretch = True)	#extract the flux of RRL/weaker line using the spatial mask in the target region


###################################################################create large spatial masks######################################################################################################
line_sigmac= {"":""}														#initiate the list of sigma values for all new convoluted maps
For cm in [2,3,4,5]:														#convolute with different multiples of beam size
	bmaj=str(imhead(imagename=line_mom0_file,mode='list')['beammajor']['value']*cm)+'arcsec'				#specify the kernel major axis length (multiples of beam size)
	bmin=str(imhead(imagename=line_mom0_file,mode='list')['beamminor']['value']*cm)+'arcsec'				#specify the kernel minor axis length
	bpa=str(imhead(imagename=line_mom0_file,mode='list')['beampa']['value'])+'deg'						#keep the kernel rotation angle as of the beam
	imsmooth(imagename=line_mom0_file,outfile=line_mom0_file+'.conv'+str(cm),major=bmaj,minor=bmin,pa=bpa,overwrite=True)	#convolute 
	line_sigmac[str(cm)] = imstat(imagename = line_mom0_file+'.conv'+str(cm), box = box)['sigma'][0]			#save the sigma values for all new convoluted maps
	exportfits(imagename=line_mom0_file+'.conv'+str(cm), fitsimage=line_mom0_file+'.conv'+str(cm)+'.fits',dropdeg=True)	#export the moment maps into FITS file		

	imview( raster= {'file':line_mom0_file,'colorwedge':True},contour=[{'file':line_mom0_file,'base':0, 'levels':[3],'unit':float(line_sigma)},{'file':line_mom0_file+'.conv'+str(cm),'base':0, 'levels':[3],'unit':line_sigmac[str(cm)]}] )												#inspect the new maps and new contour



	mask=line_mom0_file +'.conv'+str(cm)+'>='+str(3*line_sigmac[str(cm)])							#create new larger sptial mask with sigma of convolved map
	logfile_line = line_name+'_-'+str(cm)+'.0sigma.txt'									#filename storing the flux of strongest line against frequency
	logfile_RRL = RRL_name+'_-'+str(cm)+'.0sigma.txt'									#filename storing the flux of RRL/weaker line against frequency
	specflux(imagename = line_file,mask = mask,box =c,logfile = logfile_line,stretch = True)				#extract the flux of strongest line using the spatial mask in the target region
	specflux(imagename = RRL_file,mask = mask,box =c,logfile = logfile_RRL,stretch = True)					#extract the flux of RRL/weaker line using the spatial mask in the target region

	mask=line_mom0_file +'.conv'+str(cm)+'>='+str(3*line_sigma)								#create new larger sptial masks with sigma of original map
	logfile_line = line_name+'_-'+str(cm)+'.5sigma.txt'									#0.5 is just a name for the different sigma used
	logfile_RRL = RRL_name+'_-'+str(cm)+'.5sigma.txt'
	specflux(imagename = line_file,mask = mask,box =c,logfile = logfile_line,stretch = True)
	specflux(imagename = RRL_file,mask = mask,box =c,logfile = logfile_RRL,stretch = True)

####################################################after determined the channel for integrating RRL/weak line in ipython file###################################################################
chans_RRL = '154~209'									#channels used for producing moment 0 map for RRL/weak line
immoments(imagename=RRL_file,chans = chans_RRL , outfile = RRL_mom0_file)		#make moment 0 map of RRL/weak line
exportfits(imagename=RRL_mom0_file, fitsimage=RRL_mom0_file+'.fits',dropdeg=True)	#convert moment 0 map to FITS file

####################################################after determined the channel for integrating strongest line in ipython file###################################################################
chans_line_new = '166~201'									#channels used for producing moment 0 map for strongest line
line_mom0_file_new = line_name+'.new.mom0'							#new name of the map
immoments(imagename=line_file,chans = chans_line_new, outfile = line_mom0_file_new)		#make moment 0 map of strongest line
exportfits(imagename=line_mom0_file_new, fitsimage=line_mom0_file_new+'.fits',dropdeg=True)	#convert moment 0 map to FITS file

#################################################################################(optional)make moment1,2 map##################################################################
imstat(imagename=RRL_file,axes=[3],box=box)["rms"].mean()					#measuring the rms noise of the image cube of RRL
 #1pixel,0.45mJy/beam

immoments(imagename=RRL_file,moments=[1],chans="154~209",outfile=RRL_file+'.mom1.3s5s',includepix=[0.45e-3*3,999],mask=RRL_mom0_file+'>'+str(4.6e-4*5),stretch=True)			#make the mom1 map of RRL (use 3 sigma limit of in image cube, and 5 sigma limit of moment0 map)
#4.6e-4 off-target box rms

immoments(imagename='NGC_3628_H30a.lineimage',moments=[2],chans="154~209",outfile=RRL_file+'.mom2.3s5s',includepix=[0.45e-3*3,999],mask=RRL_mom0_file+'>'+str(4.6e-4*5),stretch=True)	#make the mom2 map of RRL (")

exportfits(imagename=RRL_file+'.mom1.3s5s', fitsimage=RRL_file+'.mom1.3s5s.fits',dropdeg=True)	#convert moment 0 map to FITS file
exportfits(imagename=RRL_file+'.mom2.3s5s', fitsimage=RRL_file+'.mom2.3s5s.fits',dropdeg=True)	#convert moment 0 map to FITS file

