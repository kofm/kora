# Kora

Kora is an open-source information management platform for plant variety examination and crop evaluation, with a particular focus on DUS and VCU testing. It provides tools for managing plant species, varieties, seed samples, test protocols, variety descriptions, field trials, observations, and other information generated throughout the crop evaluation lifecycle. 

Kora is designed around UPOV/Bioversity International crop characterization and variety examination standards, while remaining flexible enough to accommodate institution-specific protocols and workflows.

The application is designed for independent deployment. It can run on a single computer, within a private network, or on an institutional server, with each installation retaining control of its own data. Kora provides a REST API for programmatic access and data exchange. Interoperability with standards and external systems is an important design objective, without requiring Kora's internal data model to reproduce the functionality of general-purpose germplasm or breeding-management platforms.

Kora is free and open-source software. This is intended not only to ensure independent access to the software and data, but also to allow institutions to adapt its workflows, conventions, and data structures to their own examination practices.

## Key features

* Manage multiple crop species and plant varieties.
* Manage seed samples, including storage position, weight, and germinability.
* Define versioned crop characterization and examination protocols.
* Create standardized variety descriptions according to a selected protocol.
* Define compatibility between states belonging to different versions of a protocol.
* Organize varieties in field layouts for crop evaluation and experimental work.
* Store quantitative varietal parameters and associated provenance.
* Import and export structured data and access application data through a REST API.
* Support independent local, network, or institutional deployment.

## Status

Kora is currently **beta software**. It is stable enough for regular use (it is currently being used in production by various Examination Offices), but the database schema and migration history may still change as the application evolves. Users should maintain current backups and review release notes before upgrading. The primary supported deployment model is a local computer or a trusted private network; internet-facing deployments are possible but are not currently the main supported configuration. No hosted Kora service is provided, and there is no guarantee of uptime, long-term support, or backward compatibility between all beta releases. Upgrades are currently supported through the documented migration path between successive released versions; skipping releases or upgrading from arbitrary development revisions may not be supported.

## License

Copyright (C) 2026 Gabriele Mongiano.

Kora is free software licensed under the GNU Affero General Public License version 3 or later (AGPL-3.0-or-later). See [LICENSE](LICENSE) for details.