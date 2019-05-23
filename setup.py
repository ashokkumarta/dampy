from distutils.core import setup
setup(
  name = 'dampy',        
  packages = ['dampy'],  
  version = '0.1',      
  license='MIT', 
  description = 'Python utility to easily work with Adobe Experience Manager (AEM) DAM. ',   
  author = 'Ashokkumar T.A',                  
  author_email = 'ashokkumar.ta@gmail.com',   
  url = 'https://github.com/ashokkumarta/dampy',   
  download_url = 'https://github.com/ashokkumarta/dampy/archive/v_01.tar.gz', 
  keywords = ['AEM', 'DAM', 'Python AEM DAM Utility'],   
  install_requires=[  
      'requests',          
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)

