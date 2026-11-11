# Development and Deployment Reflection

My main implementation challenge was keeping the existing authentication behavior while meeting the requirement that the database stores a `password_hash`, not a plaintext password. The model now hashes passwords
assigned through the legacy `password` interface and registration hashes passwords explicitly. Tests verify both successful and unsuccessful password checks and confirm that the public read schema does not serialize the hash.

I also found that the model and database module declared separate SQLAlchemy metadata bases. The test fixtures were clearing tables from one base while the user table belonged to the other, which caused records to leak between tests. Using one shared base fixed the root cause and makes test isolation meaningful.

The deployment workflow now uses a PostgreSQL service for the full test suite, installs Chromium for the browser tests, scans the built image before deploy,
and only pushes Docker Hub images after successful checks on `main`. The deployment depends on the repository's `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets, so those must be configured before a successful
remote push.

Building the image also exposed incompatible dependency pins: the project requires Python 3.11, and its direct `cffi` pin conflicted with the pinned `cryptography` version. I aligned the runtime and allowed `python-jose` to resolve its compatible `pyasn1` version. A local Docker build and healthy container run now verify the image outside GitHub Actions.
