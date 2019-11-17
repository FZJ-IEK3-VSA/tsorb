[![Build Status](https://img.shields.io/gitlab/pipeline/l-kotzur/tsorb/master.svg)](https://gitlab.com/l-kotzur/tsorb/pipelines)
[![Version](https://img.shields.io/pypi/v/tsorb.svg)](https://pypi.python.org/pypi/tsorb)


<a href="https://www.fz-juelich.de/iek/iek-3/EN/Forschung/_Process-and-System-Analysis/_node.html"><img src="https://www.fz-juelich.de/SharedDocs/Bilder/INM/INM-1/EN/FZj_Logo.jpg?__blob=normal" alt="Forschungszentrum Juelich Logo" width="230px"></a> 


# tsorb - Time Series of Occupants in Residential Buildings 

*tsorb* is a python module derived from the first version of the CREST Demand Model [1,2,3]. It was updated with four state occupancy data [4] and validated for Germany [5]. It creates time series of occupancy activity and device load in residential buildings.

## Installation
Directly install via pip as follows:

	pip install tsorb

Alternatively, clone a local copy of the repository to your computer

	git clone https://github.com/FZJ-IEK3-VSA/tsorb.git
	
Then install tsorb via pip as follow
	
	cd tsorb
	pip install . 


## License

Copyright (C) 2008, 2011 Ian Richardson*, Murray Thomson*, Eoghan McKenna*
   2016 Nils Becker, 2018 Leander Kotzur**, Kevin Knosala**, Peter Stenzel**, Peter Markewitz**, Martin Robinius**, Detlef Stolten**

   *CREST (Centre for Renewable Energy Systems Technology),
   Department of Electronic and Electrical Engineering
   Loughborough University, Leicestershire LE11 3TU, UK

   ** Institute of Electrochemical Process Engineering (IEK-3), Forschungszentrum Jueulich GmbH, Wilhelm-Johnen-Str., 52428 Juelich, Germany

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.


## References

[1] Richardson, I., Thomson, M., and Infield, D. A high-resolution domestic building occupancy model for energy demand simulations. Energy and Buildings, 40(8):1560–1566, 2008. ISSN 03787788. doi: 10.1016/j.enbuild.2008.02.006.

[2] Richardson, I., Thomson, M., Infield, D., and Delahunty, A. Domestic lighting: A high-resolution energy demand model. Energy and Buildings, 41(7):781–789, 2009. ISSN 03787788. doi: 10.1016/j.enbuild.2009.02.010.

[3] Richardson, I., Thomson, M., Infield, D., and Clifford, C. Domestic electricity use: A high-resolution energy demand model. Energy and Buildings, 42(10):1878–1887, 2010. ISSN 03787788. doi: 10.1016/j.enbuild.2010.05.023.

[4] McKenna, E. and Thomson, M. High-resolution stochastic integrated thermal–electrical domestic demand model. Applied Energy, 165:445–461, 2016.ISSN 03062619. doi: 10.1016/j.apenergy.2015.12.089.

[5] Kotzur, L. [Future grid load of the residential building sector](http://juser.fz-juelich.de/record/858675). Thesis, 2018. isbn: 978-3-95806-370-9,