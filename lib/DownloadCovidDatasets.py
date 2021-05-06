import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from urllib.request import urlretrieve



class DownloadCovidDatasets:
	"""
	The ``DownloadCovidDatasets`` module
	====================================

	Use it to download COVID-19 datasets and related. You can download the Hopkins Univertity datasets,
	Paraná Health's Secretary dataset or even datasets containing Paraná cities with IBGE code 
	and Paranavaí region cities with IBGE code.

	Obs: All methods of the class class are static.

	:Example: 

	>>> from lib.DownloadCovidDatasets import DownloadCovidDatasets
	>>> DownloadCovidDatasets.downloadParanaDataset()
	"""
	
	__urlHopkinsDatasets = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_#VAR1#_global.csv'
	__urlParanaDataset = 'https://www.saude.pr.gov.br/sites/default/arquivos_restritos/files/documento/#VAR1#/informe_epidemiologico_#VAR2#_geral.csv'
	__urlOwnDatasets = 'https://raw.githubusercontent.com/FlavioLucasFer/datascience/master/datasets/#VAR1#.csv'
	__datasetsDir = './datasets-covid'
	
	@classmethod
	def __getUrlHopkinsDatasets(self):
		"""
		Get default URL to download Hopkins University datasets 
		like global COVID-19 confirmed cases by day.

		The default URL contain '#VAR1#', it mean that the URL vary 
		on this local, based on which dataset you want to download

		:return: Default URL to to download Hopkins University datasets 
		:rtype: string

		:Example:
		>>> self.__getUrlHopkinsDatasets()
		"""
		return self.__urlHopkinsDatasets

	@classmethod
	def getUrlHopkinsGlobalConfirmedCases(self):
		"""
		Get URL to download global confirmed cases of COVID-19 dataset, 
		made available by Hopkins University

		:return: URL to download global confirmed cases of COVID-19 dataset
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.getUrlHopkinsGlobalConfirmedCases
		"""
		return self.__getUrlHopkinsDatasets().replace('#VAR1#', 'confirmed')

	@classmethod
	def getUrlHopkinsGlobalDeaths(self):
		"""
		Get URL to download global deaths by COVID-19 dataset, 
		made available by Hopkins University

		:return: URL to download global deaths by COVID-19 dataset
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.getUrlHopkinsGlobalDeaths
		"""
		return self.__getUrlHopkinsDatasets().replace('#VAR1#', 'deaths')
	
	@classmethod
	def getUrlHopkinsGlobalRecovered(self):
		"""
		Get URL to download global recovered of COVID-19 dataset, 
		made available by Hopkins University

		:return: URL to download global recovered of COVID-19 dataset
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.getUrlHopkinsGlobalRecovered
		"""
		return self.__getUrlHopkinsDatasets().replace('#VAR1#', 'recovered')
	
	@classmethod
	def getUrlParanaDataset(self):
		"""
		Get default URL to download COVID-19 cases in Paraná state dataset,
		made avaliable by Paraná Health's Secretary

		The default URL contain '#VAR1#' and '#VAR2#', it mean that the URL vary 
		on this locals, based on dataset update date

		:return: URL to download COVID-19 cases in Paraná state dataset
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.getUrlParanaDataset
		"""
		return self.__urlParanaDataset

	@classmethod
	def __setUrlParanaDataset(self, yearAndMonth, targetDate):
		"""
		Set URL to download COVID-19 cases in Paraná state

		:param yearAndMonth: The year and month of dataset, at format '%Y-%m'
		:param targetDate: the target date of dataset you want to download, at format '%d_%m_%Y'
		:type yearAndMonth: string
		:type targetDate: string
		:return: returns nothing
		:rtype: void

		:Example:

		>>> self.__setUrlParanaDataset()
		"""
		self.__urlParanaDataset = self.__urlParanaDataset.replace('#VAR1#', yearAndMonth).replace('#VAR2#', targetDate)

	@classmethod
	def __getUrlOwnDatasets(self):
		"""
		Get default URL to download datasets provided by the class author

		The default URL contain '#VAR1#', it mean that the URL vary 
		on this local, based on which dataset you want to download

		:return: Default URL to download class author datasets
		:rtype: string

		:Example:

		>>> self.__getUrlOwnDatasets
		"""
		return self.__urlOwnDatasets

	@classmethod
	def getDatasetsDir(self):
		"""
		Get datasets directory

		:return: Datasets directory
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.getDatasetsDir
		"""
		return self.__datasetsDir

	@classmethod
	def setDatasetsDir(self, datasetsDir):
		"""
		Set datasets directory

		:param datasetsDir: The directory you want to save datasets
		:type datasetsDir: string 
		:return: returns nothing
		:rtype: void

		:Example:

		>>> DownloadCovidDatasets.getDatasetsDir
		"""
		self.__datasetsDir = datasetsDir
	
	@classmethod
	def checkDatasetDir(self, datasetsDir):
		"""
		Check if datasets directory exists

		:param datasetsDir: The directory you want to check. Default: './datasets-covid'
		:type datasetsDir: string
		:return: True if dataset directory exists, else False
		:rtype: boolean

		:Example:

		>>> DownloadCovidDatasets.checkDatasetDir
		"""
		datasetsDir = datasetsDir if datasetsDir else self.__datasetsDir
		
		if os.path.isdir(datasetsDir):
			return True
		
		return False
	
	@classmethod
	def checkDataset(self, datasetName, datasetsDir=''):
		"""
		Check if dataset exists

		:param datasetName: The name of dataset you want to check
		:param datasetsDir: The directory of datasets. Default: './datasets-covid'
		:type datasetName: string
		:type datasetsDir: string
		:return: True if dataset exists, else False
		:rtype: boolean

		:Example:

		>>> DownloadCovidDatasets.checkDataset
		"""

		datasetsDir = datasetsDir if datasetsDir else self.__datasetsDir
		datasetPath = f'{datasetsDir}/{datasetName}'

		if os.path.isfile(datasetPath):
			return True

		return False
	
	@classmethod
	def downloadDataset(self, url, dirToSave, csvFileName, overwrite=False):
		"""
		Download dataset from internet

		:param url: The URL to download dataset
		:param dirToSave: The directory to save the dataset
		:param csvFileName: The name of csv file
		:param overwrite: Overwrite dataset if already exists. Default: False
		:type url: string
		:type dirToSave: string
		:type csvFileName: string
		:type overwrite: boolean
		:return: Dataset path
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.downloadDataset
		"""
		datasetPath = f'{dirToSave}/{csvFileName}'

		if not self.checkDatasetDir(dirToSave):
			os.mkdir(dirToSave)
		else:
			print(f"The target directory '{dirToSave}' already exists.")

		print('Url:', url)

		if not self.checkDataset(csvFileName, dirToSave) or overwrite:
			print('Downloading csv file...')
			urlretrieve(url, datasetPath)
			print('Download success!')

		else:
			print(f"Csv file '{csvFileName}' already downloaded!")
		
		print('Dataset path:', datasetPath)

		return datasetPath

	@classmethod
	def downloadParanaDataset(self, csvFileName='daily_newsletter_covid_parana', tDate='', dirToSave='', csvFileNameWithTDate=False, overwrite=False):
		"""
		Download COVID-19 cases in Paraná State

		:param csvFileName: The name of csv file. Default: 'daily_newsletter_covid_parana.csv'
		:param tDate: The target date of dataset you want to download, at format '%d/%m/%Y'. Default: Current date
		:param dirToSave: The directory to save the dataset. Default: './datasets-covid'
		:param csvFileNameWithTDate: If you want dataset date on csv file name. Default: False
		:param overwrite: Overwrite dataset if already exists. Default: False
		:type csvFileName: string
		:type tDate: string
		:type dirToSave: string
		:type csvFileNameWithTDate: boolean
		:type overwrite: boolean
		:return: Dataset path
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.downloadParanaDataset
		"""

		yearAndMonth = ''
		targetDate = ''
		dirToSave = dirToSave if dirToSave else self.getDatasetsDir()

		if (tDate):
			date = tDate.split('/')
			yearAndMonth = f'{date[2]}-{date[1]}'
			targetDate = f'{date[0]}_{date[1]}_{date[2]}'

		else:
			now = datetime.now()
			currentTime = now.replace(hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)
			paranaDatasetUpdateHour = now.replace(hour=15, minute=0, second=0, microsecond=0)
			yearAndMonth = now.strftime('%Y-%m')

			if currentTime >= paranaDatasetUpdateHour:
				targetDate = now.strftime('%d_%m_%Y')
			else:
				targetDate = (now - timedelta(days=1)).strftime('%d_%m_%Y')

		self.__setUrlParanaDataset(yearAndMonth, targetDate)
		
		if csvFileNameWithTDate:
			csvFileName += f'_{targetDate}.csv'
		else:
			csvFileName += '.csv'

		return self.downloadDataset(self.getUrlParanaDataset(), dirToSave, csvFileName, overwrite)
	
	@classmethod
	def downloadHopkinsDataset(self, csvFileName='hopkins_global_', kind='confirmed', dirToSave='', csvFileNameWithTDate=False, overwrite=False):
		"""
		Download global COVID-19 dataset provided by Hopkins University

		:param csvFileName: The name of csv file. Default: 'hopkins_global_' + kind + '.csv'
		:param kind: Dataset of confirmed cases, deaths or recovered. 
		Accepted values: confirmed, deaths and recovered. Default: confirmed 
		:param dirToSave: The directory to save the dataset. Default: './datasets-covid'
		:param csvFileNameWithTDate: If you want dataset date on csv file name: Default: False
		:param overwrite: Overwrite dataset if already exists. Default: False
		:type csvFileName: string
		:type kind: string
		:type dirToSave: string
		:type csvFileNameWithTDate: boolean
		:type overwrite: boolean
		:return: Dataset path
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.downloadHopkinsDataset
		"""
		
		dirToSave = dirToSave if dirToSave else self.getDatasetsDir()

		if kind.lower() == 'confirmed':
			csvFileName += 'confirmed_cases'
		elif kind.lower() == 'deaths':
			csvFileName += 'deaths'
		elif kind.lower() == 'recovered':
			csvFileName += 'recovered'
		else:
			print("Kind argument only suports: 'confirmed', 'deaths' or 'recovered' values!")

		if csvFileNameWithTDate:
			today = datetime.now().strftime('%d_%m_%Y')
			csvFileName += f'_{today}.csv'
		else:
			csvFileName += '.csv'
		
		url = self.getUrlHopkinsGlobalConfirmedCases().replace('#VAR1#', kind)

		return self.downloadDataset(url, dirToSave, csvFileName, overwrite)
	
	@classmethod
	def downloadParanaCitiesWithIBGECodeDataset(self, csvFileName='parana_cities_with_ibge_code.csv', dirToSave='', overwrite=False):
		"""
		Download Paraná cities with IBGE code dataset, provided by class author

		:param csvFileName: The name of csv file. Default: 'parana_cities_with_ibge_code.csv'
		:param dirToSave: The directory to save the dataset. Default: './datasets-covid'
		:param overwrite: Overwrite dataset if already exists. Default: False
		:type csvFileName: string
		:type dirToSave: string
		:type overwrite: boolean
		:return: Dataset path
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.downloadParanaCitiesWithIBGECodeDataset
		"""
		dirToSave = dirToSave if dirToSave else self.getDatasetsDir()

		url = self.__getUrlOwnDatasets().replace('#VAR1#', 'parana_cities_with_ibge_code')

		return self.downloadDataset(url, dirToSave, csvFileName, overwrite)
	
	@classmethod
	def downloadParanavaiRegionCitiesWithIBGECodeDataset(self, csvFileName='paranavai_region_cities_with_ibge_code.csv', dirToSave='', overwrite=False):
		"""
		Download Paranavaí region cities with IBGE code dataset, provided by class author

		:param csvFileName: The name of csv file. Default: 'paranavai_region_cities_with_ibge_code.csv'
		:param dirToSave: The directory to save the dataset. Default: './datasets-covid'
		:param overwrite: Overwrite dataset if already exists. Default: False
		:type csvFileName: string
		:type dirToSave: string
		:type overwrite: boolean
		:return: Dataset path
		:rtype: string

		:Example:

		>>> DownloadCovidDatasets.downloadParanavaiRegionCitiesWithIBGECodeDataset
		"""
		dirToSave = dirToSave if dirToSave else self.getDatasetsDir()

		url = self.__getUrlOwnDatasets().replace('#VAR1#', 'parana_cities_with_ibge_code')

		return self.downloadDataset(url, dirToSave, csvFileName, overwrite)
		
