Kora is a local-first web application written in Django, designed for
managing plant genetic resources (PGRs) and germplasm collections,
particularly for cultivated crops. It provides a streamlined and
standardized approach to genetic material management, fully compatible
with Biodiversity International and UPOV guidelines. The software
enables users to build a comprehensive database, storing passport
data, characterization data following descriptor lists, and
information specific to the reproductive material like storage
location, germinability, and weight.

The software was created to address the various challenges related the
storage, management, analysis, and explotation of PGR. It ensures that
high-standard data collection can be shared efficiently, reducing
inconsistencies in genetic resource management. The software is
particularly beneficial for conservationists, researchers, DUS and VCU
experts, plant breeders managing genetic material during genetic
improvement programs, and farmers or individuals interested in
biodiversity.

Designed with a "local first" approach, the software is containerized
using Docker, allowing local installation without requiring a
dedicated internet-based server. It supports data interchangeability
between different instances, facilitating collaboration and
flexibility. Additionally, it incorporates simple user management
functionalities, with separate viewing and administrator roles.

Future development plans focus on further integration of crop modeling
capabilities, enabling users to implement or utilize crop models from
an existing library. These models could make use the stored
characterization and evaluation data as input parameters. Users will
also be able to create zones, such as trial locations, and associate
weather or other environmental data with these zones to execute crop
models within specific locations.

The software is already stable and fully usable but remains under
continuous development to introduce new functionalities and
improvements.

# Key features

- Store and manage data related to multiple crop species.
- Describe species using user-definable crop descriptors, following
  Bioversity International or UPOV methodology.
- Store crop observations and biometrics, and use them to derive crop
  parameters.
- Manage zones and areas defined as geolocalized containers linking crops,
  weather data (public APIs and IoT sensors), and management data.
- Utilities to implement simple crop models leveraging the database.
