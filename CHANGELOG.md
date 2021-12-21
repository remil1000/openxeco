# Change Log
All notable changes to this project will be documented in this file.

## [1.7.0] - 2022-01-06
  
Update the database structure bu using the following command:
- flask db upgrade

### Added

- Dockerization configuration
- GitHub Action to deploy bo-api container
- flask_migrate with replicated structure in the first revision
- Initial user creation and configuration for start of new instance
- private/generate_mu_user_handle resource
 
### Changed
  
- Rename application.py to app.py
- Rename application.wsgi to wsgi.py
- Database structure defined on 54992185f712 revision
- Request process when a user subscribe with company info
- Unit testing environment to be adapted to the new config system
 
### Fixed
 
-
