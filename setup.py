# ashokkumar.ta@gmail.com / 24-May-2019
from distutils.core import setup
setup(
  name = 'dampy',        
  packages = ['dampy'],  
  version = '0.2',      
  license='MIT', 
  description = 'A python tool to easily work with Adobe Experience Manager (AEM) DAM. ',   
  author = 'Ashokkumar T.A',                  
  author_email = 'ashokkumar.ta@gmail.com',   
  url = 'https://github.com/ashokkumarta/dampy',   
  download_url = 'https://github.com/ashokkumarta/dampy/archive/0.2.tar.gz', 
  keywords = ['AEM', 'DAM', 'Python tool', 'list', 'create', 'upload', 'download', 'activate', 'deactivate', 'delete'],   
  install_requires=[  
      'requests',          
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
