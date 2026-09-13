# Kora

Kora is an open-source information management system for plant variety characterization and evaluation, with a particular focus on DUS and VCU testing. It provides tools for managing variety descriptions, seed samples, legal status, field trials, observations, and other information generated throughout the crop evaluation lifecycle. Kora is designed around UPOV/Bioversity International crop characterization and variety examination standards, while remaining flexible enough to accommodate different workflows.

## Key features

* Manage multiple crop species and plant varieties.
* Manage seed samples, including storage position, weight, and germinability.
* Define crop characterization and examination protocols.
* Create standardized variety descriptions according to a selected protocol.
* Define compatibility between states of expression belonging to different versions of a protocol.
* Organize varieties in field layouts for crop evaluation and experimental work.
* Store quantitative varietal parameters.
* Import spreadsheet data and access application data through a REST API.

The primary supported deployment model is a local computer or a trusted private network; internet-facing deployments are possible but are not currently the main supported configuration. See the [documentation](https://docs.getkora.org).

## Status

Kora is currently **beta software**. It is stable enough for regular use, but the database schema and migration history may still change as the application evolves. Users should maintain current backups and review release notes before upgrading. 

## License

Copyright (C) 2026 Gabriele Mongiano.

Kora is free software licensed under the GNU Affero General Public License version 3 or later (AGPL-3.0-or-later). See [LICENSE](LICENSE) for details.
