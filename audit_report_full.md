# Full Source Audit Bundle

Generated: Sun, Jul 20, 2025 00:50:04 UTC

## Repository Tree (truncated)

```
.env
.env.example
.gitattributes
.github
.github/dependabot.yml
.github/workflows
.github/workflows/ci.yml
.github/workflows/codeql.yml
.github/workflows/pyproject.toml
.gitignore
.pre-commit-config.yaml
.pytest_cache
.pytest_cache/.gitignore
.pytest_cache/CACHEDIR.TAG
.pytest_cache/README.md
.pytest_cache/v
.pytest_cache/v/cache
.pytest_cache/v/cache/lastfailed
.pytest_cache/v/cache/nodeids
alembic.ini
app
app/__init__.py
app/archivist.py
app/cli.py
app/db.py
app/endpoints.py
app/logging_config.py
app/main.py
app/models.py
app/schemas.py
app/security.py
audit_full.md
audit_report.md
docker-compose.yml
Dockerfile
eventbus.db
LICENSE
migrations
migrations/env.py
migrations/README
migrations/script.py.mako
migrations/versions
migrations/versions/bd536313df34_create_audit_log.py
mosquitto
mosquitto/certs
mosquitto/certs/ca.crt
mosquitto/certs/ca.key
mosquitto/certs/ca.srl
mosquitto/certs/server.crt
mosquitto/certs/server.csr
mosquitto/certs/server.key
mosquitto/conf
mosquitto/conf/mosquitto.conf
projects_data
projects_data/FC-008c3925-fd41-42a6-bf98-651c7872b6fd
projects_data/FC-008c3925-fd41-42a6-bf98-651c7872b6fd/01_raw_data
projects_data/FC-008c3925-fd41-42a6-bf98-651c7872b6fd/02_processed_data
projects_data/FC-008c3925-fd41-42a6-bf98-651c7872b6fd/03_reports
projects_data/FC-02a65910-b3b9-47f4-9b7a-735b440633e3
projects_data/FC-02a65910-b3b9-47f4-9b7a-735b440633e3/01_raw_data
projects_data/FC-02a65910-b3b9-47f4-9b7a-735b440633e3/02_processed_data
projects_data/FC-02a65910-b3b9-47f4-9b7a-735b440633e3/03_reports
projects_data/FC-0326d7ee-69be-49d6-a497-0e753d14cef2
projects_data/FC-0326d7ee-69be-49d6-a497-0e753d14cef2/01_raw_data
projects_data/FC-0326d7ee-69be-49d6-a497-0e753d14cef2/02_processed_data
projects_data/FC-0326d7ee-69be-49d6-a497-0e753d14cef2/03_reports
projects_data/FC-03920aed-e56d-4a82-b1f4-6a7827754bae
projects_data/FC-03920aed-e56d-4a82-b1f4-6a7827754bae/01_raw_data
projects_data/FC-03920aed-e56d-4a82-b1f4-6a7827754bae/02_processed_data
projects_data/FC-03920aed-e56d-4a82-b1f4-6a7827754bae/03_reports
projects_data/FC-04d43996-92be-4b93-8ef6-eb2e3efd99f4
projects_data/FC-04d43996-92be-4b93-8ef6-eb2e3efd99f4/01_raw_data
projects_data/FC-04d43996-92be-4b93-8ef6-eb2e3efd99f4/02_processed_data
projects_data/FC-04d43996-92be-4b93-8ef6-eb2e3efd99f4/03_reports
projects_data/FC-04deb657-0980-41fb-b674-396b32d740ef
projects_data/FC-04deb657-0980-41fb-b674-396b32d740ef/01_raw_data
projects_data/FC-04deb657-0980-41fb-b674-396b32d740ef/02_processed_data
projects_data/FC-04deb657-0980-41fb-b674-396b32d740ef/03_reports
projects_data/FC-05729d7f-3ec8-45eb-a4b4-ad0acbcc29d6
projects_data/FC-05729d7f-3ec8-45eb-a4b4-ad0acbcc29d6/01_raw_data
projects_data/FC-05729d7f-3ec8-45eb-a4b4-ad0acbcc29d6/02_processed_data
projects_data/FC-05729d7f-3ec8-45eb-a4b4-ad0acbcc29d6/03_reports
projects_data/FC-0c543dda-27ac-43c0-bf37-4190826c14ec
projects_data/FC-0c543dda-27ac-43c0-bf37-4190826c14ec/01_raw_data
projects_data/FC-0c543dda-27ac-43c0-bf37-4190826c14ec/02_processed_data
projects_data/FC-0c543dda-27ac-43c0-bf37-4190826c14ec/03_reports
projects_data/FC-0c55cf0f-497a-426e-bcc6-de69da4849bb
projects_data/FC-0c55cf0f-497a-426e-bcc6-de69da4849bb/01_raw_data
projects_data/FC-0c55cf0f-497a-426e-bcc6-de69da4849bb/02_processed_data
projects_data/FC-0c55cf0f-497a-426e-bcc6-de69da4849bb/03_reports
projects_data/FC-0dc72fdb-dd1d-4a13-9b3c-2a5e3d6be90c
projects_data/FC-0dc72fdb-dd1d-4a13-9b3c-2a5e3d6be90c/01_raw_data
projects_data/FC-0dc72fdb-dd1d-4a13-9b3c-2a5e3d6be90c/02_processed_data
projects_data/FC-0dc72fdb-dd1d-4a13-9b3c-2a5e3d6be90c/03_reports
projects_data/FC-0e491943-1933-48c2-84a9-13cb20452b20
projects_data/FC-0e491943-1933-48c2-84a9-13cb20452b20/01_raw_data
projects_data/FC-0e491943-1933-48c2-84a9-13cb20452b20/02_processed_data
projects_data/FC-0e491943-1933-48c2-84a9-13cb20452b20/03_reports
projects_data/FC-0eccf164-0f0a-407e-9d80-a5da91ffa853
projects_data/FC-0eccf164-0f0a-407e-9d80-a5da91ffa853/01_raw_data
projects_data/FC-0eccf164-0f0a-407e-9d80-a5da91ffa853/02_processed_data
projects_data/FC-0eccf164-0f0a-407e-9d80-a5da91ffa853/03_reports
projects_data/FC-0f90ce38-cf98-43df-9aa2-39618406317b
projects_data/FC-0f90ce38-cf98-43df-9aa2-39618406317b/01_raw_data
projects_data/FC-0f90ce38-cf98-43df-9aa2-39618406317b/02_processed_data
projects_data/FC-0f90ce38-cf98-43df-9aa2-39618406317b/03_reports
projects_data/FC-1102b1e2-bcc0-40b3-b335-ff43042a166f
projects_data/FC-1102b1e2-bcc0-40b3-b335-ff43042a166f/01_raw_data
projects_data/FC-1102b1e2-bcc0-40b3-b335-ff43042a166f/02_processed_data
projects_data/FC-1102b1e2-bcc0-40b3-b335-ff43042a166f/03_reports
projects_data/FC-1267552d-b112-414e-9b25-31c54855969c
projects_data/FC-1267552d-b112-414e-9b25-31c54855969c/01_raw_data
projects_data/FC-1267552d-b112-414e-9b25-31c54855969c/02_processed_data
projects_data/FC-1267552d-b112-414e-9b25-31c54855969c/03_reports
projects_data/FC-128047ff-6387-4d1e-8064-64388e2ec68e
projects_data/FC-128047ff-6387-4d1e-8064-64388e2ec68e/01_raw_data
projects_data/FC-128047ff-6387-4d1e-8064-64388e2ec68e/02_processed_data
projects_data/FC-128047ff-6387-4d1e-8064-64388e2ec68e/03_reports
projects_data/FC-12a0000c-56b9-4d4a-9fc4-746603a7982e
projects_data/FC-12a0000c-56b9-4d4a-9fc4-746603a7982e/01_raw_data
projects_data/FC-12a0000c-56b9-4d4a-9fc4-746603a7982e/02_processed_data
projects_data/FC-12a0000c-56b9-4d4a-9fc4-746603a7982e/03_reports
projects_data/FC-13d22caa-a976-4d8e-9bca-f2e596d1ac32
projects_data/FC-13d22caa-a976-4d8e-9bca-f2e596d1ac32/01_raw_data
projects_data/FC-13d22caa-a976-4d8e-9bca-f2e596d1ac32/02_processed_data
projects_data/FC-13d22caa-a976-4d8e-9bca-f2e596d1ac32/03_reports
projects_data/FC-144f22f5-4213-4534-be5b-dbbfca3aa226
projects_data/FC-144f22f5-4213-4534-be5b-dbbfca3aa226/01_raw_data
projects_data/FC-144f22f5-4213-4534-be5b-dbbfca3aa226/02_processed_data
projects_data/FC-144f22f5-4213-4534-be5b-dbbfca3aa226/03_reports
projects_data/FC-15a05651-2ebc-4d7a-b51d-489d02282f2a
projects_data/FC-15a05651-2ebc-4d7a-b51d-489d02282f2a/01_raw_data
projects_data/FC-15a05651-2ebc-4d7a-b51d-489d02282f2a/02_processed_data
projects_data/FC-15a05651-2ebc-4d7a-b51d-489d02282f2a/03_reports
projects_data/FC-170c5a3c-4d85-4b28-9871-9d1931039071
projects_data/FC-170c5a3c-4d85-4b28-9871-9d1931039071/01_raw_data
projects_data/FC-170c5a3c-4d85-4b28-9871-9d1931039071/02_processed_data
projects_data/FC-170c5a3c-4d85-4b28-9871-9d1931039071/03_reports
projects_data/FC-175c4972-bfed-4137-bd49-a88baad9bd11
projects_data/FC-175c4972-bfed-4137-bd49-a88baad9bd11/01_raw_data
projects_data/FC-175c4972-bfed-4137-bd49-a88baad9bd11/02_processed_data
projects_data/FC-175c4972-bfed-4137-bd49-a88baad9bd11/03_reports
projects_data/FC-17d10e55-1497-4796-8a74-e8cae95233f9
projects_data/FC-17d10e55-1497-4796-8a74-e8cae95233f9/01_raw_data
projects_data/FC-17d10e55-1497-4796-8a74-e8cae95233f9/02_processed_data
projects_data/FC-17d10e55-1497-4796-8a74-e8cae95233f9/03_reports
projects_data/FC-1db7b79c-0989-46e1-8b19-ef41f6269eed
projects_data/FC-1db7b79c-0989-46e1-8b19-ef41f6269eed/01_raw_data
projects_data/FC-1db7b79c-0989-46e1-8b19-ef41f6269eed/02_processed_data
projects_data/FC-1db7b79c-0989-46e1-8b19-ef41f6269eed/03_reports
projects_data/FC-1f6fed1a-2fe8-469f-a5b9-4df1ecebf582
projects_data/FC-1f6fed1a-2fe8-469f-a5b9-4df1ecebf582/01_raw_data
projects_data/FC-1f6fed1a-2fe8-469f-a5b9-4df1ecebf582/02_processed_data
projects_data/FC-1f6fed1a-2fe8-469f-a5b9-4df1ecebf582/03_reports
projects_data/FC-1fd26e47-4146-4f58-9130-9e5458d6784e
projects_data/FC-1fd26e47-4146-4f58-9130-9e5458d6784e/01_raw_data
projects_data/FC-1fd26e47-4146-4f58-9130-9e5458d6784e/02_processed_data
projects_data/FC-1fd26e47-4146-4f58-9130-9e5458d6784e/03_reports
projects_data/FC-1fe573b2-bea9-4941-b51f-2b0f40023866
projects_data/FC-1fe573b2-bea9-4941-b51f-2b0f40023866/01_raw_data
projects_data/FC-1fe573b2-bea9-4941-b51f-2b0f40023866/02_processed_data
projects_data/FC-1fe573b2-bea9-4941-b51f-2b0f40023866/03_reports
projects_data/FC-20cba19f-4e66-464e-afb5-a31a8ad3c206
projects_data/FC-20cba19f-4e66-464e-afb5-a31a8ad3c206/01_raw_data
projects_data/FC-20cba19f-4e66-464e-afb5-a31a8ad3c206/02_processed_data
projects_data/FC-20cba19f-4e66-464e-afb5-a31a8ad3c206/03_reports
projects_data/FC-21312525-4f4c-48f6-8033-1d4f5f719055
projects_data/FC-21312525-4f4c-48f6-8033-1d4f5f719055/01_raw_data
projects_data/FC-21312525-4f4c-48f6-8033-1d4f5f719055/02_processed_data
projects_data/FC-21312525-4f4c-48f6-8033-1d4f5f719055/03_reports
projects_data/FC-22027c35-e08b-4cd2-8085-659f2706587d
projects_data/FC-22027c35-e08b-4cd2-8085-659f2706587d/01_raw_data
projects_data/FC-22027c35-e08b-4cd2-8085-659f2706587d/02_processed_data
projects_data/FC-22027c35-e08b-4cd2-8085-659f2706587d/03_reports
projects_data/FC-226b6770-bfe3-41d6-b424-8b7f7d3de2d6
projects_data/FC-226b6770-bfe3-41d6-b424-8b7f7d3de2d6/01_raw_data
projects_data/FC-226b6770-bfe3-41d6-b424-8b7f7d3de2d6/02_processed_data
projects_data/FC-226b6770-bfe3-41d6-b424-8b7f7d3de2d6/03_reports
projects_data/FC-2341a7eb-8c00-49ea-9bf6-473a38a81366
projects_data/FC-2341a7eb-8c00-49ea-9bf6-473a38a81366/01_raw_data
projects_data/FC-2341a7eb-8c00-49ea-9bf6-473a38a81366/02_processed_data
projects_data/FC-2341a7eb-8c00-49ea-9bf6-473a38a81366/03_reports
projects_data/FC-244a6297-ac76-4dda-8956-50504a58853f
projects_data/FC-244a6297-ac76-4dda-8956-50504a58853f/01_raw_data
projects_data/FC-244a6297-ac76-4dda-8956-50504a58853f/02_processed_data
projects_data/FC-244a6297-ac76-4dda-8956-50504a58853f/03_reports
projects_data/FC-247b3333-53f4-45a1-a743-f447e3eb9fb8
projects_data/FC-247b3333-53f4-45a1-a743-f447e3eb9fb8/01_raw_data
projects_data/FC-247b3333-53f4-45a1-a743-f447e3eb9fb8/02_processed_data
projects_data/FC-247b3333-53f4-45a1-a743-f447e3eb9fb8/03_reports
projects_data/FC-24cf8fd8-386f-44d0-ac5c-3cb03b957e50
projects_data/FC-24cf8fd8-386f-44d0-ac5c-3cb03b957e50/01_raw_data
projects_data/FC-24cf8fd8-386f-44d0-ac5c-3cb03b957e50/02_processed_data
projects_data/FC-24cf8fd8-386f-44d0-ac5c-3cb03b957e50/03_reports
projects_data/FC-28969c71-b118-4e31-a8f3-47a4acd7f35c
projects_data/FC-28969c71-b118-4e31-a8f3-47a4acd7f35c/01_raw_data
projects_data/FC-28969c71-b118-4e31-a8f3-47a4acd7f35c/02_processed_data
projects_data/FC-28969c71-b118-4e31-a8f3-47a4acd7f35c/03_reports
projects_data/FC-29859a9f-6921-4d14-970c-b165f521c49e
projects_data/FC-29859a9f-6921-4d14-970c-b165f521c49e/01_raw_data
projects_data/FC-29859a9f-6921-4d14-970c-b165f521c49e/02_processed_data
projects_data/FC-29859a9f-6921-4d14-970c-b165f521c49e/03_reports
projects_data/FC-2d5a2392-c718-477a-8d75-af2bce8761ab
projects_data/FC-2d5a2392-c718-477a-8d75-af2bce8761ab/01_raw_data
projects_data/FC-2d5a2392-c718-477a-8d75-af2bce8761ab/02_processed_data
projects_data/FC-2d5a2392-c718-477a-8d75-af2bce8761ab/03_reports
projects_data/FC-2def1ad7-33c7-4af2-b455-59c7251b82a6
projects_data/FC-2def1ad7-33c7-4af2-b455-59c7251b82a6/01_raw_data
projects_data/FC-2def1ad7-33c7-4af2-b455-59c7251b82a6/02_processed_data
projects_data/FC-2def1ad7-33c7-4af2-b455-59c7251b82a6/03_reports
projects_data/FC-3181ed7c-b07e-4539-95a9-299adbafe312
projects_data/FC-3181ed7c-b07e-4539-95a9-299adbafe312/01_raw_data
projects_data/FC-3181ed7c-b07e-4539-95a9-299adbafe312/02_processed_data
projects_data/FC-3181ed7c-b07e-4539-95a9-299adbafe312/03_reports
projects_data/FC-32f50fff-f4ae-485c-869e-048dd8dbca38
projects_data/FC-32f50fff-f4ae-485c-869e-048dd8dbca38/01_raw_data
projects_data/FC-32f50fff-f4ae-485c-869e-048dd8dbca38/02_processed_data
projects_data/FC-32f50fff-f4ae-485c-869e-048dd8dbca38/03_reports
projects_data/FC-33a212e7-b8ec-4afd-a51e-6436cfb9b46e
projects_data/FC-33a212e7-b8ec-4afd-a51e-6436cfb9b46e/01_raw_data
projects_data/FC-33a212e7-b8ec-4afd-a51e-6436cfb9b46e/02_processed_data
projects_data/FC-33a212e7-b8ec-4afd-a51e-6436cfb9b46e/03_reports
projects_data/FC-35724fc3-bd9b-42ff-8fce-8fc88a53aacb
projects_data/FC-35724fc3-bd9b-42ff-8fce-8fc88a53aacb/01_raw_data
projects_data/FC-35724fc3-bd9b-42ff-8fce-8fc88a53aacb/02_processed_data
projects_data/FC-35724fc3-bd9b-42ff-8fce-8fc88a53aacb/03_reports
projects_data/FC-36336dc1-4a26-4934-95aa-2c5243583942
projects_data/FC-36336dc1-4a26-4934-95aa-2c5243583942/01_raw_data
projects_data/FC-36336dc1-4a26-4934-95aa-2c5243583942/02_processed_data
projects_data/FC-36336dc1-4a26-4934-95aa-2c5243583942/03_reports
projects_data/FC-36493c0e-1758-42ba-9709-7af21b301928
projects_data/FC-36493c0e-1758-42ba-9709-7af21b301928/01_raw_data
projects_data/FC-36493c0e-1758-42ba-9709-7af21b301928/02_processed_data
projects_data/FC-36493c0e-1758-42ba-9709-7af21b301928/03_reports
projects_data/FC-365c0cc3-a92b-4960-8d7a-2b8c0c490735
projects_data/FC-365c0cc3-a92b-4960-8d7a-2b8c0c490735/01_raw_data
projects_data/FC-365c0cc3-a92b-4960-8d7a-2b8c0c490735/02_processed_data
projects_data/FC-365c0cc3-a92b-4960-8d7a-2b8c0c490735/03_reports
projects_data/FC-36bb4557-634a-4c1f-a6f4-12d7374b82a6
projects_data/FC-36bb4557-634a-4c1f-a6f4-12d7374b82a6/01_raw_data
projects_data/FC-36bb4557-634a-4c1f-a6f4-12d7374b82a6/02_processed_data
projects_data/FC-36bb4557-634a-4c1f-a6f4-12d7374b82a6/03_reports
projects_data/FC-3b289d91-6ee1-44d7-8bc4-122788a7eac6
projects_data/FC-3b289d91-6ee1-44d7-8bc4-122788a7eac6/01_raw_data
projects_data/FC-3b289d91-6ee1-44d7-8bc4-122788a7eac6/02_processed_data
projects_data/FC-3b289d91-6ee1-44d7-8bc4-122788a7eac6/03_reports
projects_data/FC-3b66e696-fa4c-461e-9e78-996ed1ca8408
projects_data/FC-3b66e696-fa4c-461e-9e78-996ed1ca8408/01_raw_data
projects_data/FC-3b66e696-fa4c-461e-9e78-996ed1ca8408/02_processed_data
projects_data/FC-3b66e696-fa4c-461e-9e78-996ed1ca8408/03_reports
projects_data/FC-3c2c9151-0636-4432-b4b1-360f688bf26e
projects_data/FC-3c2c9151-0636-4432-b4b1-360f688bf26e/01_raw_data
projects_data/FC-3c2c9151-0636-4432-b4b1-360f688bf26e/02_processed_data
projects_data/FC-3c2c9151-0636-4432-b4b1-360f688bf26e/03_reports
projects_data/FC-3c5e5709-b6e6-49d5-9ad6-517f2da551f7
projects_data/FC-3c5e5709-b6e6-49d5-9ad6-517f2da551f7/01_raw_data
projects_data/FC-3c5e5709-b6e6-49d5-9ad6-517f2da551f7/02_processed_data
projects_data/FC-3c5e5709-b6e6-49d5-9ad6-517f2da551f7/03_reports
projects_data/FC-3f898d8b-c711-4ad6-92af-ffdf25d839b4
projects_data/FC-3f898d8b-c711-4ad6-92af-ffdf25d839b4/01_raw_data
projects_data/FC-3f898d8b-c711-4ad6-92af-ffdf25d839b4/02_processed_data
projects_data/FC-3f898d8b-c711-4ad6-92af-ffdf25d839b4/03_reports
projects_data/FC-415db839-6bb1-4aff-a6b6-2312d166d4db
projects_data/FC-415db839-6bb1-4aff-a6b6-2312d166d4db/01_raw_data
projects_data/FC-415db839-6bb1-4aff-a6b6-2312d166d4db/02_processed_data
projects_data/FC-415db839-6bb1-4aff-a6b6-2312d166d4db/03_reports
projects_data/FC-42e81460-5508-473a-9acc-32bd2709a414
projects_data/FC-42e81460-5508-473a-9acc-32bd2709a414/01_raw_data
projects_data/FC-42e81460-5508-473a-9acc-32bd2709a414/02_processed_data
projects_data/FC-42e81460-5508-473a-9acc-32bd2709a414/03_reports
projects_data/FC-462d6dd2-fe4e-4f7d-b0a6-fdd91ed4db4d
projects_data/FC-462d6dd2-fe4e-4f7d-b0a6-fdd91ed4db4d/01_raw_data
projects_data/FC-462d6dd2-fe4e-4f7d-b0a6-fdd91ed4db4d/02_processed_data
projects_data/FC-462d6dd2-fe4e-4f7d-b0a6-fdd91ed4db4d/03_reports
projects_data/FC-46ed321c-9019-464e-9cfc-18b1aee476d1
projects_data/FC-46ed321c-9019-464e-9cfc-18b1aee476d1/01_raw_data
projects_data/FC-46ed321c-9019-464e-9cfc-18b1aee476d1/02_processed_data
projects_data/FC-46ed321c-9019-464e-9cfc-18b1aee476d1/03_reports
projects_data/FC-470e3b9b-c36b-4800-a858-99814521f2b1
projects_data/FC-470e3b9b-c36b-4800-a858-99814521f2b1/01_raw_data
projects_data/FC-470e3b9b-c36b-4800-a858-99814521f2b1/02_processed_data
projects_data/FC-470e3b9b-c36b-4800-a858-99814521f2b1/03_reports
projects_data/FC-47c9d522-83d9-4e25-942f-f90e0cf4493b
projects_data/FC-47c9d522-83d9-4e25-942f-f90e0cf4493b/01_raw_data
projects_data/FC-47c9d522-83d9-4e25-942f-f90e0cf4493b/02_processed_data
projects_data/FC-47c9d522-83d9-4e25-942f-f90e0cf4493b/03_reports
projects_data/FC-48333c01-f7c0-44a0-b567-48eedd936e13
projects_data/FC-48333c01-f7c0-44a0-b567-48eedd936e13/01_raw_data
projects_data/FC-48333c01-f7c0-44a0-b567-48eedd936e13/02_processed_data
projects_data/FC-48333c01-f7c0-44a0-b567-48eedd936e13/03_reports
projects_data/FC-48a5c6ba-0fda-491e-87da-65a6d9b39157
projects_data/FC-48a5c6ba-0fda-491e-87da-65a6d9b39157/01_raw_data
projects_data/FC-48a5c6ba-0fda-491e-87da-65a6d9b39157/02_processed_data
projects_data/FC-48a5c6ba-0fda-491e-87da-65a6d9b39157/03_reports
projects_data/FC-4999a58e-5298-4c34-b168-9f68fee981b2
projects_data/FC-4999a58e-5298-4c34-b168-9f68fee981b2/01_raw_data
projects_data/FC-4999a58e-5298-4c34-b168-9f68fee981b2/02_processed_data
projects_data/FC-4999a58e-5298-4c34-b168-9f68fee981b2/03_reports
projects_data/FC-4aa166e9-9c2b-4c11-8cd3-474139396ba7
projects_data/FC-4aa166e9-9c2b-4c11-8cd3-474139396ba7/01_raw_data
projects_data/FC-4aa166e9-9c2b-4c11-8cd3-474139396ba7/02_processed_data
projects_data/FC-4aa166e9-9c2b-4c11-8cd3-474139396ba7/03_reports
projects_data/FC-4c39e663-e7c9-49ea-8551-597c0495fd4d
projects_data/FC-4c39e663-e7c9-49ea-8551-597c0495fd4d/01_raw_data
projects_data/FC-4c39e663-e7c9-49ea-8551-597c0495fd4d/02_processed_data
projects_data/FC-4c39e663-e7c9-49ea-8551-597c0495fd4d/03_reports
projects_data/FC-4e1a0cc6-26db-4f62-bed9-65a763a687e4
projects_data/FC-4e1a0cc6-26db-4f62-bed9-65a763a687e4/01_raw_data
projects_data/FC-4e1a0cc6-26db-4f62-bed9-65a763a687e4/02_processed_data
projects_data/FC-4e1a0cc6-26db-4f62-bed9-65a763a687e4/03_reports
projects_data/FC-4e509ab1-e701-4d39-8a89-95a73c87f71d
projects_data/FC-4e509ab1-e701-4d39-8a89-95a73c87f71d/01_raw_data
projects_data/FC-4e509ab1-e701-4d39-8a89-95a73c87f71d/02_processed_data
projects_data/FC-4e509ab1-e701-4d39-8a89-95a73c87f71d/03_reports
projects_data/FC-4e72ad23-d819-432e-af1e-e40b02ade408
projects_data/FC-4e72ad23-d819-432e-af1e-e40b02ade408/01_raw_data
projects_data/FC-4e72ad23-d819-432e-af1e-e40b02ade408/02_processed_data
projects_data/FC-4e72ad23-d819-432e-af1e-e40b02ade408/03_reports
projects_data/FC-4f106f5a-61a3-47d7-ab42-74300a2ccaed
projects_data/FC-4f106f5a-61a3-47d7-ab42-74300a2ccaed/01_raw_data
projects_data/FC-4f106f5a-61a3-47d7-ab42-74300a2ccaed/02_processed_data
projects_data/FC-4f106f5a-61a3-47d7-ab42-74300a2ccaed/03_reports
projects_data/FC-5231a02c-463f-4acb-9449-8bb8b2700001
projects_data/FC-5231a02c-463f-4acb-9449-8bb8b2700001/01_raw_data
projects_data/FC-5231a02c-463f-4acb-9449-8bb8b2700001/02_processed_data
projects_data/FC-5231a02c-463f-4acb-9449-8bb8b2700001/03_reports
projects_data/FC-524702f5-b7a2-47cf-bf90-6d0906d9a0ad
projects_data/FC-524702f5-b7a2-47cf-bf90-6d0906d9a0ad/01_raw_data
projects_data/FC-524702f5-b7a2-47cf-bf90-6d0906d9a0ad/02_processed_data
projects_data/FC-524702f5-b7a2-47cf-bf90-6d0906d9a0ad/03_reports
projects_data/FC-5297b25a-19d9-49da-8480-da14dc3a4826
projects_data/FC-5297b25a-19d9-49da-8480-da14dc3a4826/01_raw_data
projects_data/FC-5297b25a-19d9-49da-8480-da14dc3a4826/02_processed_data
projects_data/FC-5297b25a-19d9-49da-8480-da14dc3a4826/03_reports
projects_data/FC-537eb34a-c549-42b6-9fe0-ee55c2383ece
projects_data/FC-537eb34a-c549-42b6-9fe0-ee55c2383ece/01_raw_data
projects_data/FC-537eb34a-c549-42b6-9fe0-ee55c2383ece/02_processed_data
projects_data/FC-537eb34a-c549-42b6-9fe0-ee55c2383ece/03_reports
projects_data/FC-54513f65-3858-4968-baf0-b7b43227bfef
projects_data/FC-54513f65-3858-4968-baf0-b7b43227bfef/01_raw_data
projects_data/FC-54513f65-3858-4968-baf0-b7b43227bfef/02_processed_data
projects_data/FC-54513f65-3858-4968-baf0-b7b43227bfef/03_reports
projects_data/FC-54820ba2-9d91-4fe3-aab7-144a6bedf41e
projects_data/FC-54820ba2-9d91-4fe3-aab7-144a6bedf41e/01_raw_data
projects_data/FC-54820ba2-9d91-4fe3-aab7-144a6bedf41e/02_processed_data
projects_data/FC-54820ba2-9d91-4fe3-aab7-144a6bedf41e/03_reports
projects_data/FC-54c09520-fa8c-4e54-9177-acddd05985bc
projects_data/FC-54c09520-fa8c-4e54-9177-acddd05985bc/01_raw_data
projects_data/FC-54c09520-fa8c-4e54-9177-acddd05985bc/02_processed_data
projects_data/FC-54c09520-fa8c-4e54-9177-acddd05985bc/03_reports
projects_data/FC-565cf2e6-308e-4726-8d13-8e05bbf36197
projects_data/FC-565cf2e6-308e-4726-8d13-8e05bbf36197/01_raw_data
projects_data/FC-565cf2e6-308e-4726-8d13-8e05bbf36197/02_processed_data
projects_data/FC-565cf2e6-308e-4726-8d13-8e05bbf36197/03_reports
projects_data/FC-568fd10f-dadb-4a03-bd0b-68c83f54554f
projects_data/FC-568fd10f-dadb-4a03-bd0b-68c83f54554f/01_raw_data
projects_data/FC-568fd10f-dadb-4a03-bd0b-68c83f54554f/02_processed_data
projects_data/FC-568fd10f-dadb-4a03-bd0b-68c83f54554f/03_reports
projects_data/FC-56c5c2ba-f77f-4b80-8791-ce79e5d2ff3d
projects_data/FC-56c5c2ba-f77f-4b80-8791-ce79e5d2ff3d/01_raw_data
projects_data/FC-56c5c2ba-f77f-4b80-8791-ce79e5d2ff3d/02_processed_data
projects_data/FC-56c5c2ba-f77f-4b80-8791-ce79e5d2ff3d/03_reports
projects_data/FC-5835c5c0-41a7-4951-a796-676d1f22ecd5
projects_data/FC-5835c5c0-41a7-4951-a796-676d1f22ecd5/01_raw_data
projects_data/FC-5835c5c0-41a7-4951-a796-676d1f22ecd5/02_processed_data
projects_data/FC-5835c5c0-41a7-4951-a796-676d1f22ecd5/03_reports
projects_data/FC-58f16f01-9afb-4eba-8264-d27689561526
projects_data/FC-58f16f01-9afb-4eba-8264-d27689561526/01_raw_data
projects_data/FC-58f16f01-9afb-4eba-8264-d27689561526/02_processed_data
projects_data/FC-58f16f01-9afb-4eba-8264-d27689561526/03_reports
projects_data/FC-59189e84-8ceb-4ea7-b7c2-8e859d7bb3cf
projects_data/FC-59189e84-8ceb-4ea7-b7c2-8e859d7bb3cf/01_raw_data
projects_data/FC-59189e84-8ceb-4ea7-b7c2-8e859d7bb3cf/02_processed_data
projects_data/FC-59189e84-8ceb-4ea7-b7c2-8e859d7bb3cf/03_reports
projects_data/FC-595fe089-b5bb-4ad4-8c8a-63691018c319
projects_data/FC-595fe089-b5bb-4ad4-8c8a-63691018c319/01_raw_data
projects_data/FC-595fe089-b5bb-4ad4-8c8a-63691018c319/02_processed_data
projects_data/FC-595fe089-b5bb-4ad4-8c8a-63691018c319/03_reports
projects_data/FC-61cb47d9-62af-4880-ad17-9be0791fef57
projects_data/FC-61cb47d9-62af-4880-ad17-9be0791fef57/01_raw_data
projects_data/FC-61cb47d9-62af-4880-ad17-9be0791fef57/02_processed_data
projects_data/FC-61cb47d9-62af-4880-ad17-9be0791fef57/03_reports
projects_data/FC-632a82ce-519c-492e-b057-3389c3a61eac
projects_data/FC-632a82ce-519c-492e-b057-3389c3a61eac/01_raw_data
projects_data/FC-632a82ce-519c-492e-b057-3389c3a61eac/02_processed_data
projects_data/FC-632a82ce-519c-492e-b057-3389c3a61eac/03_reports
projects_data/FC-64943bea-c8ea-4255-a296-faec9538e055
projects_data/FC-64943bea-c8ea-4255-a296-faec9538e055/01_raw_data
projects_data/FC-64943bea-c8ea-4255-a296-faec9538e055/02_processed_data
projects_data/FC-64943bea-c8ea-4255-a296-faec9538e055/03_reports
projects_data/FC-65fbf849-85b1-4502-bab5-a164088377d1
projects_data/FC-65fbf849-85b1-4502-bab5-a164088377d1/01_raw_data
projects_data/FC-65fbf849-85b1-4502-bab5-a164088377d1/02_processed_data
projects_data/FC-65fbf849-85b1-4502-bab5-a164088377d1/03_reports
projects_data/FC-68cce00f-0ea3-4cb6-98a6-83720a43dcd5
projects_data/FC-68cce00f-0ea3-4cb6-98a6-83720a43dcd5/01_raw_data
projects_data/FC-68cce00f-0ea3-4cb6-98a6-83720a43dcd5/02_processed_data
projects_data/FC-68cce00f-0ea3-4cb6-98a6-83720a43dcd5/03_reports
projects_data/FC-690c11ad-6114-4b2c-9989-47d07744ae86
projects_data/FC-690c11ad-6114-4b2c-9989-47d07744ae86/01_raw_data
projects_data/FC-690c11ad-6114-4b2c-9989-47d07744ae86/02_processed_data
projects_data/FC-690c11ad-6114-4b2c-9989-47d07744ae86/03_reports
projects_data/FC-6b9be132-9b42-410e-b9e2-eb6c3e26f67c
projects_data/FC-6b9be132-9b42-410e-b9e2-eb6c3e26f67c/01_raw_data
projects_data/FC-6b9be132-9b42-410e-b9e2-eb6c3e26f67c/02_processed_data
projects_data/FC-6b9be132-9b42-410e-b9e2-eb6c3e26f67c/03_reports
projects_data/FC-6e45d3c0-596a-43e4-98df-f40348e3ab11
projects_data/FC-6e45d3c0-596a-43e4-98df-f40348e3ab11/01_raw_data
projects_data/FC-6e45d3c0-596a-43e4-98df-f40348e3ab11/02_processed_data
projects_data/FC-6e45d3c0-596a-43e4-98df-f40348e3ab11/03_reports
projects_data/FC-7094f017-8a16-4dbb-8275-c0953c933be3
projects_data/FC-7094f017-8a16-4dbb-8275-c0953c933be3/01_raw_data
projects_data/FC-7094f017-8a16-4dbb-8275-c0953c933be3/02_processed_data
projects_data/FC-7094f017-8a16-4dbb-8275-c0953c933be3/03_reports
projects_data/FC-7280be8a-6ce2-448a-ada5-271fa3076618
projects_data/FC-7280be8a-6ce2-448a-ada5-271fa3076618/01_raw_data
projects_data/FC-7280be8a-6ce2-448a-ada5-271fa3076618/02_processed_data
projects_data/FC-7280be8a-6ce2-448a-ada5-271fa3076618/03_reports
projects_data/FC-72e3544a-3440-411c-a797-f180440a3c50
projects_data/FC-72e3544a-3440-411c-a797-f180440a3c50/01_raw_data
projects_data/FC-72e3544a-3440-411c-a797-f180440a3c50/02_processed_data
projects_data/FC-72e3544a-3440-411c-a797-f180440a3c50/03_reports
projects_data/FC-73af5142-773c-4c01-85a4-f235435b04e9
projects_data/FC-73af5142-773c-4c01-85a4-f235435b04e9/01_raw_data
projects_data/FC-73af5142-773c-4c01-85a4-f235435b04e9/02_processed_data
projects_data/FC-73af5142-773c-4c01-85a4-f235435b04e9/03_reports
projects_data/FC-743fc9de-be1b-4fb1-ae6e-db6ba108caf5
projects_data/FC-743fc9de-be1b-4fb1-ae6e-db6ba108caf5/01_raw_data
projects_data/FC-743fc9de-be1b-4fb1-ae6e-db6ba108caf5/02_processed_data
projects_data/FC-743fc9de-be1b-4fb1-ae6e-db6ba108caf5/03_reports
projects_data/FC-7507dd8f-3cf5-4e81-a461-f27e64e224ae
projects_data/FC-7507dd8f-3cf5-4e81-a461-f27e64e224ae/01_raw_data
projects_data/FC-7507dd8f-3cf5-4e81-a461-f27e64e224ae/02_processed_data
projects_data/FC-7507dd8f-3cf5-4e81-a461-f27e64e224ae/03_reports
projects_data/FC-7625e77e-9243-4150-a4e3-3c4998805b6e
projects_data/FC-7625e77e-9243-4150-a4e3-3c4998805b6e/01_raw_data
projects_data/FC-7625e77e-9243-4150-a4e3-3c4998805b6e/02_processed_data
projects_data/FC-7625e77e-9243-4150-a4e3-3c4998805b6e/03_reports
projects_data/FC-764a7e9a-ffd0-4a3e-b955-bbbaf9a93f25
projects_data/FC-764a7e9a-ffd0-4a3e-b955-bbbaf9a93f25/01_raw_data
projects_data/FC-764a7e9a-ffd0-4a3e-b955-bbbaf9a93f25/02_processed_data
projects_data/FC-764a7e9a-ffd0-4a3e-b955-bbbaf9a93f25/03_reports
projects_data/FC-7694f48c-cf27-4172-adf3-41b3ca515fc5
projects_data/FC-7694f48c-cf27-4172-adf3-41b3ca515fc5/01_raw_data
projects_data/FC-7694f48c-cf27-4172-adf3-41b3ca515fc5/02_processed_data
projects_data/FC-7694f48c-cf27-4172-adf3-41b3ca515fc5/03_reports
projects_data/FC-76ae7c42-68ad-494e-9f2d-cbc5d87cc1b1
projects_data/FC-76ae7c42-68ad-494e-9f2d-cbc5d87cc1b1/01_raw_data
projects_data/FC-76ae7c42-68ad-494e-9f2d-cbc5d87cc1b1/02_processed_data
projects_data/FC-76ae7c42-68ad-494e-9f2d-cbc5d87cc1b1/03_reports
projects_data/FC-76c77a52-4ccd-40cf-926f-d3704f0e468e
projects_data/FC-76c77a52-4ccd-40cf-926f-d3704f0e468e/01_raw_data
projects_data/FC-76c77a52-4ccd-40cf-926f-d3704f0e468e/02_processed_data
projects_data/FC-76c77a52-4ccd-40cf-926f-d3704f0e468e/03_reports
projects_data/FC-77c76631-ab50-4953-b941-76bf136459f4
projects_data/FC-77c76631-ab50-4953-b941-76bf136459f4/01_raw_data
projects_data/FC-77c76631-ab50-4953-b941-76bf136459f4/02_processed_data
projects_data/FC-77c76631-ab50-4953-b941-76bf136459f4/03_reports
projects_data/FC-780423bd-7da0-4603-917d-8444fb7dcace
projects_data/FC-780423bd-7da0-4603-917d-8444fb7dcace/01_raw_data
projects_data/FC-780423bd-7da0-4603-917d-8444fb7dcace/02_processed_data
projects_data/FC-780423bd-7da0-4603-917d-8444fb7dcace/03_reports
projects_data/FC-7a86b23c-3939-4d9e-8922-1b5e862c3d44
projects_data/FC-7a86b23c-3939-4d9e-8922-1b5e862c3d44/01_raw_data
projects_data/FC-7a86b23c-3939-4d9e-8922-1b5e862c3d44/02_processed_data
projects_data/FC-7a86b23c-3939-4d9e-8922-1b5e862c3d44/03_reports
projects_data/FC-7c7ad766-24dc-42ec-80ca-3015c77d03cc
projects_data/FC-7c7ad766-24dc-42ec-80ca-3015c77d03cc/01_raw_data
projects_data/FC-7c7ad766-24dc-42ec-80ca-3015c77d03cc/02_processed_data
projects_data/FC-7c7ad766-24dc-42ec-80ca-3015c77d03cc/03_reports
projects_data/FC-84353693-9b4b-44ae-a086-94c08b80c724
projects_data/FC-84353693-9b4b-44ae-a086-94c08b80c724/01_raw_data
projects_data/FC-84353693-9b4b-44ae-a086-94c08b80c724/02_processed_data
projects_data/FC-84353693-9b4b-44ae-a086-94c08b80c724/03_reports
projects_data/FC-85784b44-5a49-4da6-bc0f-d21c16b4daf3
projects_data/FC-85784b44-5a49-4da6-bc0f-d21c16b4daf3/01_raw_data
projects_data/FC-85784b44-5a49-4da6-bc0f-d21c16b4daf3/02_processed_data
projects_data/FC-85784b44-5a49-4da6-bc0f-d21c16b4daf3/03_reports
projects_data/FC-86478e62-a947-4af3-83aa-9c7f34f45298
projects_data/FC-86478e62-a947-4af3-83aa-9c7f34f45298/01_raw_data
projects_data/FC-86478e62-a947-4af3-83aa-9c7f34f45298/02_processed_data
projects_data/FC-86478e62-a947-4af3-83aa-9c7f34f45298/03_reports
projects_data/FC-8832cd82-5707-438f-a96c-93f65e92a07c
projects_data/FC-8832cd82-5707-438f-a96c-93f65e92a07c/01_raw_data
projects_data/FC-8832cd82-5707-438f-a96c-93f65e92a07c/02_processed_data
projects_data/FC-8832cd82-5707-438f-a96c-93f65e92a07c/03_reports
projects_data/FC-8a830bd1-4022-46eb-a86e-a9c918197a62
projects_data/FC-8a830bd1-4022-46eb-a86e-a9c918197a62/01_raw_data
projects_data/FC-8a830bd1-4022-46eb-a86e-a9c918197a62/02_processed_data
projects_data/FC-8a830bd1-4022-46eb-a86e-a9c918197a62/03_reports
projects_data/FC-8c54ddd9-513b-48ee-a197-69c31a173208
projects_data/FC-8c54ddd9-513b-48ee-a197-69c31a173208/01_raw_data
projects_data/FC-8c54ddd9-513b-48ee-a197-69c31a173208/02_processed_data
projects_data/FC-8c54ddd9-513b-48ee-a197-69c31a173208/03_reports
projects_data/FC-8d20e638-7370-4c06-938b-bd12fb792263
projects_data/FC-8d20e638-7370-4c06-938b-bd12fb792263/01_raw_data
projects_data/FC-8d20e638-7370-4c06-938b-bd12fb792263/02_processed_data
projects_data/FC-8d20e638-7370-4c06-938b-bd12fb792263/03_reports
projects_data/FC-8e08521e-3c18-48b7-bb77-1e4a8305d672
projects_data/FC-8e08521e-3c18-48b7-bb77-1e4a8305d672/01_raw_data
projects_data/FC-8e08521e-3c18-48b7-bb77-1e4a8305d672/02_processed_data
projects_data/FC-8e08521e-3c18-48b7-bb77-1e4a8305d672/03_reports
projects_data/FC-9154f464-9302-4818-9a50-31e1d805a90d
projects_data/FC-9154f464-9302-4818-9a50-31e1d805a90d/01_raw_data
projects_data/FC-9154f464-9302-4818-9a50-31e1d805a90d/02_processed_data
projects_data/FC-9154f464-9302-4818-9a50-31e1d805a90d/03_reports
projects_data/FC-94802e65-b356-44b9-8431-00562426cf03
projects_data/FC-94802e65-b356-44b9-8431-00562426cf03/01_raw_data
projects_data/FC-94802e65-b356-44b9-8431-00562426cf03/02_processed_data
projects_data/FC-94802e65-b356-44b9-8431-00562426cf03/03_reports
projects_data/FC-94b6fe31-178f-4369-b3ef-8d4590dfcb22
projects_data/FC-94b6fe31-178f-4369-b3ef-8d4590dfcb22/01_raw_data
projects_data/FC-94b6fe31-178f-4369-b3ef-8d4590dfcb22/02_processed_data
projects_data/FC-94b6fe31-178f-4369-b3ef-8d4590dfcb22/03_reports
projects_data/FC-95af0978-fb7c-4fd8-984b-86ebe3a211b8
projects_data/FC-95af0978-fb7c-4fd8-984b-86ebe3a211b8/01_raw_data
projects_data/FC-95af0978-fb7c-4fd8-984b-86ebe3a211b8/02_processed_data
projects_data/FC-95af0978-fb7c-4fd8-984b-86ebe3a211b8/03_reports
projects_data/FC-96116a82-44f5-47cf-913e-a19ea0102e4c
projects_data/FC-96116a82-44f5-47cf-913e-a19ea0102e4c/01_raw_data
projects_data/FC-96116a82-44f5-47cf-913e-a19ea0102e4c/02_processed_data
projects_data/FC-96116a82-44f5-47cf-913e-a19ea0102e4c/03_reports
projects_data/FC-97192e8c-6346-47e6-87e0-7b3056c09816
projects_data/FC-97192e8c-6346-47e6-87e0-7b3056c09816/01_raw_data
projects_data/FC-97192e8c-6346-47e6-87e0-7b3056c09816/02_processed_data
projects_data/FC-97192e8c-6346-47e6-87e0-7b3056c09816/03_reports
projects_data/FC-97aaac2d-bed5-4a35-af4a-5c0ffce81745
projects_data/FC-97aaac2d-bed5-4a35-af4a-5c0ffce81745/01_raw_data
projects_data/FC-97aaac2d-bed5-4a35-af4a-5c0ffce81745/02_processed_data
projects_data/FC-97aaac2d-bed5-4a35-af4a-5c0ffce81745/03_reports
projects_data/FC-991cbf1c-2c15-44e5-9ee2-eae8270a210d
projects_data/FC-991cbf1c-2c15-44e5-9ee2-eae8270a210d/01_raw_data
projects_data/FC-991cbf1c-2c15-44e5-9ee2-eae8270a210d/02_processed_data
projects_data/FC-991cbf1c-2c15-44e5-9ee2-eae8270a210d/03_reports
projects_data/FC-992aa2f4-ab94-4c9a-b56f-6398df7c2fe1
projects_data/FC-992aa2f4-ab94-4c9a-b56f-6398df7c2fe1/01_raw_data
projects_data/FC-992aa2f4-ab94-4c9a-b56f-6398df7c2fe1/02_processed_data
projects_data/FC-992aa2f4-ab94-4c9a-b56f-6398df7c2fe1/03_reports
projects_data/FC-9a11fd27-6206-498c-8324-d4b29decce98
projects_data/FC-9a11fd27-6206-498c-8324-d4b29decce98/01_raw_data
projects_data/FC-9a11fd27-6206-498c-8324-d4b29decce98/02_processed_data
projects_data/FC-9a11fd27-6206-498c-8324-d4b29decce98/03_reports
projects_data/FC-9a18b48c-1d4a-4cc9-94e2-771551e7bf70
projects_data/FC-9a18b48c-1d4a-4cc9-94e2-771551e7bf70/01_raw_data
projects_data/FC-9a18b48c-1d4a-4cc9-94e2-771551e7bf70/02_processed_data
projects_data/FC-9a18b48c-1d4a-4cc9-94e2-771551e7bf70/03_reports
projects_data/FC-9c32decb-aa37-4081-a023-e23c791ecc79
projects_data/FC-9c32decb-aa37-4081-a023-e23c791ecc79/01_raw_data
projects_data/FC-9c32decb-aa37-4081-a023-e23c791ecc79/02_processed_data
projects_data/FC-9c32decb-aa37-4081-a023-e23c791ecc79/03_reports
projects_data/FC-9cfc8206-cf5c-4c93-8ae8-8e4ef6ac5285
projects_data/FC-9cfc8206-cf5c-4c93-8ae8-8e4ef6ac5285/01_raw_data
projects_data/FC-9cfc8206-cf5c-4c93-8ae8-8e4ef6ac5285/02_processed_data
projects_data/FC-9cfc8206-cf5c-4c93-8ae8-8e4ef6ac5285/03_reports
projects_data/FC-9dd89ded-4aad-424a-95b9-76c787e65581
projects_data/FC-9dd89ded-4aad-424a-95b9-76c787e65581/01_raw_data
projects_data/FC-9dd89ded-4aad-424a-95b9-76c787e65581/02_processed_data
projects_data/FC-9dd89ded-4aad-424a-95b9-76c787e65581/03_reports
projects_data/FC-9e3a21be-f0c4-461f-ba0c-9b18556d07ed
projects_data/FC-9e3a21be-f0c4-461f-ba0c-9b18556d07ed/01_raw_data
projects_data/FC-9e3a21be-f0c4-461f-ba0c-9b18556d07ed/02_processed_data
projects_data/FC-9e3a21be-f0c4-461f-ba0c-9b18556d07ed/03_reports
projects_data/FC-9e79048b-1583-42db-ad25-b31dd2950588
projects_data/FC-9e79048b-1583-42db-ad25-b31dd2950588/01_raw_data
projects_data/FC-9e79048b-1583-42db-ad25-b31dd2950588/02_processed_data
projects_data/FC-9e79048b-1583-42db-ad25-b31dd2950588/03_reports
projects_data/FC-9ea60c98-778e-4a4f-ba14-6ac24dbe4ee3
projects_data/FC-9ea60c98-778e-4a4f-ba14-6ac24dbe4ee3/01_raw_data
projects_data/FC-9ea60c98-778e-4a4f-ba14-6ac24dbe4ee3/02_processed_data
projects_data/FC-9ea60c98-778e-4a4f-ba14-6ac24dbe4ee3/03_reports
projects_data/FC-9eba8da4-f19d-4d97-b6c8-07a30973693b
projects_data/FC-9eba8da4-f19d-4d97-b6c8-07a30973693b/01_raw_data
projects_data/FC-9eba8da4-f19d-4d97-b6c8-07a30973693b/02_processed_data
projects_data/FC-9eba8da4-f19d-4d97-b6c8-07a30973693b/03_reports
projects_data/FC-9fbd439a-740d-414d-b939-17124cfd181a
projects_data/FC-9fbd439a-740d-414d-b939-17124cfd181a/01_raw_data
projects_data/FC-9fbd439a-740d-414d-b939-17124cfd181a/02_processed_data
projects_data/FC-9fbd439a-740d-414d-b939-17124cfd181a/03_reports
projects_data/FC-a70ea85c-0d7c-43fa-bc77-e39c9c938d76
projects_data/FC-a70ea85c-0d7c-43fa-bc77-e39c9c938d76/01_raw_data
projects_data/FC-a70ea85c-0d7c-43fa-bc77-e39c9c938d76/02_processed_data
projects_data/FC-a70ea85c-0d7c-43fa-bc77-e39c9c938d76/03_reports
projects_data/FC-abbcd2af-7358-4885-9acf-ee671c83cbb7
projects_data/FC-abbcd2af-7358-4885-9acf-ee671c83cbb7/01_raw_data
projects_data/FC-abbcd2af-7358-4885-9acf-ee671c83cbb7/02_processed_data
projects_data/FC-abbcd2af-7358-4885-9acf-ee671c83cbb7/03_reports
projects_data/FC-ac50dffc-57b3-4b23-8449-5c4418b35aea
projects_data/FC-ac50dffc-57b3-4b23-8449-5c4418b35aea/01_raw_data
projects_data/FC-ac50dffc-57b3-4b23-8449-5c4418b35aea/02_processed_data
projects_data/FC-ac50dffc-57b3-4b23-8449-5c4418b35aea/03_reports
projects_data/FC-ae6e0e10-8865-4013-a862-c179ab5e3a9a
projects_data/FC-ae6e0e10-8865-4013-a862-c179ab5e3a9a/01_raw_data
projects_data/FC-ae6e0e10-8865-4013-a862-c179ab5e3a9a/02_processed_data
projects_data/FC-ae6e0e10-8865-4013-a862-c179ab5e3a9a/03_reports
projects_data/FC-af63d865-6156-47b1-a547-d15c373e49ef
projects_data/FC-af63d865-6156-47b1-a547-d15c373e49ef/01_raw_data
projects_data/FC-af63d865-6156-47b1-a547-d15c373e49ef/02_processed_data
projects_data/FC-af63d865-6156-47b1-a547-d15c373e49ef/03_reports
projects_data/FC-b117f49a-8023-4636-a9ce-a748ea1b82f2
projects_data/FC-b117f49a-8023-4636-a9ce-a748ea1b82f2/01_raw_data
projects_data/FC-b117f49a-8023-4636-a9ce-a748ea1b82f2/02_processed_data
projects_data/FC-b117f49a-8023-4636-a9ce-a748ea1b82f2/03_reports
projects_data/FC-b352abf9-b3f4-4fef-8bb3-642e925b638d
projects_data/FC-b352abf9-b3f4-4fef-8bb3-642e925b638d/01_raw_data
projects_data/FC-b352abf9-b3f4-4fef-8bb3-642e925b638d/02_processed_data
projects_data/FC-b352abf9-b3f4-4fef-8bb3-642e925b638d/03_reports
projects_data/FC-b3a5aba2-0105-4d51-aabb-97e6b49bf7ef
projects_data/FC-b3a5aba2-0105-4d51-aabb-97e6b49bf7ef/01_raw_data
projects_data/FC-b3a5aba2-0105-4d51-aabb-97e6b49bf7ef/02_processed_data
projects_data/FC-b3a5aba2-0105-4d51-aabb-97e6b49bf7ef/03_reports
projects_data/FC-b6e750d9-db31-48ed-8b28-e35c9efa1f21
projects_data/FC-b6e750d9-db31-48ed-8b28-e35c9efa1f21/01_raw_data
projects_data/FC-b6e750d9-db31-48ed-8b28-e35c9efa1f21/02_processed_data
projects_data/FC-b6e750d9-db31-48ed-8b28-e35c9efa1f21/03_reports
projects_data/FC-b722364c-2503-453f-8e9e-f0dbf56638ce
projects_data/FC-b722364c-2503-453f-8e9e-f0dbf56638ce/01_raw_data
projects_data/FC-b722364c-2503-453f-8e9e-f0dbf56638ce/02_processed_data
projects_data/FC-b722364c-2503-453f-8e9e-f0dbf56638ce/03_reports
projects_data/FC-b76a2e69-5b17-4f9c-8326-0601682c3a89
projects_data/FC-b76a2e69-5b17-4f9c-8326-0601682c3a89/01_raw_data
projects_data/FC-b76a2e69-5b17-4f9c-8326-0601682c3a89/02_processed_data
projects_data/FC-b76a2e69-5b17-4f9c-8326-0601682c3a89/03_reports
projects_data/FC-b7e6cdcd-a01f-4e8d-91d9-ec287203fcce
projects_data/FC-b7e6cdcd-a01f-4e8d-91d9-ec287203fcce/01_raw_data
projects_data/FC-b7e6cdcd-a01f-4e8d-91d9-ec287203fcce/02_processed_data
projects_data/FC-b7e6cdcd-a01f-4e8d-91d9-ec287203fcce/03_reports
projects_data/FC-b9760e9a-5242-4a83-82d1-863a5b7f2ad4
projects_data/FC-b9760e9a-5242-4a83-82d1-863a5b7f2ad4/01_raw_data
projects_data/FC-b9760e9a-5242-4a83-82d1-863a5b7f2ad4/02_processed_data
projects_data/FC-b9760e9a-5242-4a83-82d1-863a5b7f2ad4/03_reports
projects_data/FC-b977370c-1c9b-4cea-9615-c00bcfddf35e
projects_data/FC-b977370c-1c9b-4cea-9615-c00bcfddf35e/01_raw_data
projects_data/FC-b977370c-1c9b-4cea-9615-c00bcfddf35e/02_processed_data
projects_data/FC-b977370c-1c9b-4cea-9615-c00bcfddf35e/03_reports
projects_data/FC-bb7ac86b-aec0-4653-bb7f-38a1f6779a0c
projects_data/FC-bb7ac86b-aec0-4653-bb7f-38a1f6779a0c/01_raw_data
projects_data/FC-bb7ac86b-aec0-4653-bb7f-38a1f6779a0c/02_processed_data
projects_data/FC-bb7ac86b-aec0-4653-bb7f-38a1f6779a0c/03_reports
projects_data/FC-bba0ca98-3ab9-41c3-ae37-1b7bd94c0a72
projects_data/FC-bba0ca98-3ab9-41c3-ae37-1b7bd94c0a72/01_raw_data
projects_data/FC-bba0ca98-3ab9-41c3-ae37-1b7bd94c0a72/02_processed_data
projects_data/FC-bba0ca98-3ab9-41c3-ae37-1b7bd94c0a72/03_reports
projects_data/FC-bccdd967-4b0e-49dc-9ac8-13cfe9aefc66
projects_data/FC-bccdd967-4b0e-49dc-9ac8-13cfe9aefc66/01_raw_data
projects_data/FC-bccdd967-4b0e-49dc-9ac8-13cfe9aefc66/02_processed_data
projects_data/FC-bccdd967-4b0e-49dc-9ac8-13cfe9aefc66/03_reports
projects_data/FC-c090f4b8-a887-4690-a132-06c750a58954
projects_data/FC-c090f4b8-a887-4690-a132-06c750a58954/01_raw_data
projects_data/FC-c090f4b8-a887-4690-a132-06c750a58954/02_processed_data
projects_data/FC-c090f4b8-a887-4690-a132-06c750a58954/03_reports
projects_data/FC-c31f21ba-b4ff-4bf4-862d-ea2de86aea44
projects_data/FC-c31f21ba-b4ff-4bf4-862d-ea2de86aea44/01_raw_data
projects_data/FC-c31f21ba-b4ff-4bf4-862d-ea2de86aea44/02_processed_data
projects_data/FC-c31f21ba-b4ff-4bf4-862d-ea2de86aea44/03_reports
projects_data/FC-c7fd7869-8a80-4d33-b182-0cd293e7a55b
projects_data/FC-c7fd7869-8a80-4d33-b182-0cd293e7a55b/01_raw_data
projects_data/FC-c7fd7869-8a80-4d33-b182-0cd293e7a55b/02_processed_data
projects_data/FC-c7fd7869-8a80-4d33-b182-0cd293e7a55b/03_reports
projects_data/FC-c82d19f4-1af2-476a-aa24-49c7358c2601
projects_data/FC-c82d19f4-1af2-476a-aa24-49c7358c2601/01_raw_data
projects_data/FC-c82d19f4-1af2-476a-aa24-49c7358c2601/02_processed_data
projects_data/FC-c82d19f4-1af2-476a-aa24-49c7358c2601/03_reports
projects_data/FC-c8b13f73-32fb-4ef4-b7a5-61cbe6c9a7f7
projects_data/FC-c8b13f73-32fb-4ef4-b7a5-61cbe6c9a7f7/01_raw_data
projects_data/FC-c8b13f73-32fb-4ef4-b7a5-61cbe6c9a7f7/02_processed_data
projects_data/FC-c8b13f73-32fb-4ef4-b7a5-61cbe6c9a7f7/03_reports
projects_data/FC-ca4d8bf5-5ccf-494f-a590-35936b5b9cbc
projects_data/FC-ca4d8bf5-5ccf-494f-a590-35936b5b9cbc/01_raw_data
projects_data/FC-ca4d8bf5-5ccf-494f-a590-35936b5b9cbc/02_processed_data
projects_data/FC-ca4d8bf5-5ccf-494f-a590-35936b5b9cbc/03_reports
projects_data/FC-cb26e59f-698f-464f-aed8-cad2e9052a51
projects_data/FC-cb26e59f-698f-464f-aed8-cad2e9052a51/01_raw_data
projects_data/FC-cb26e59f-698f-464f-aed8-cad2e9052a51/02_processed_data
projects_data/FC-cb26e59f-698f-464f-aed8-cad2e9052a51/03_reports
projects_data/FC-cdbdb6d4-690a-40de-b741-ea3a7cfe23b8
projects_data/FC-cdbdb6d4-690a-40de-b741-ea3a7cfe23b8/01_raw_data
projects_data/FC-cdbdb6d4-690a-40de-b741-ea3a7cfe23b8/02_processed_data
projects_data/FC-cdbdb6d4-690a-40de-b741-ea3a7cfe23b8/03_reports
projects_data/FC-cf61ebad-51ac-4997-993f-6a1c58cca8e8
projects_data/FC-cf61ebad-51ac-4997-993f-6a1c58cca8e8/01_raw_data
projects_data/FC-cf61ebad-51ac-4997-993f-6a1c58cca8e8/02_processed_data
projects_data/FC-cf61ebad-51ac-4997-993f-6a1c58cca8e8/03_reports
projects_data/FC-d02ac54a-ea1e-4d81-b5fc-b2399925088e
projects_data/FC-d02ac54a-ea1e-4d81-b5fc-b2399925088e/01_raw_data
projects_data/FC-d02ac54a-ea1e-4d81-b5fc-b2399925088e/02_processed_data
projects_data/FC-d02ac54a-ea1e-4d81-b5fc-b2399925088e/03_reports
projects_data/FC-d1179ce6-b3f8-460a-8404-dba331e59488
projects_data/FC-d1179ce6-b3f8-460a-8404-dba331e59488/01_raw_data
projects_data/FC-d1179ce6-b3f8-460a-8404-dba331e59488/02_processed_data
projects_data/FC-d1179ce6-b3f8-460a-8404-dba331e59488/03_reports
projects_data/FC-d1a4e560-54fb-454a-9208-9c80a2a11fbd
projects_data/FC-d1a4e560-54fb-454a-9208-9c80a2a11fbd/01_raw_data
projects_data/FC-d1a4e560-54fb-454a-9208-9c80a2a11fbd/02_processed_data
projects_data/FC-d1a4e560-54fb-454a-9208-9c80a2a11fbd/03_reports
projects_data/FC-d311a904-3c92-46ff-93bf-8163e720f070
projects_data/FC-d311a904-3c92-46ff-93bf-8163e720f070/01_raw_data
projects_data/FC-d311a904-3c92-46ff-93bf-8163e720f070/02_processed_data
projects_data/FC-d311a904-3c92-46ff-93bf-8163e720f070/03_reports
projects_data/FC-d3ba0c3a-f2c2-4f06-a7ba-e474ee6ab0af
projects_data/FC-d3ba0c3a-f2c2-4f06-a7ba-e474ee6ab0af/01_raw_data
projects_data/FC-d3ba0c3a-f2c2-4f06-a7ba-e474ee6ab0af/02_processed_data
projects_data/FC-d3ba0c3a-f2c2-4f06-a7ba-e474ee6ab0af/03_reports
projects_data/FC-d645e6a2-c939-45aa-ae1e-35dfb30f174e
projects_data/FC-d645e6a2-c939-45aa-ae1e-35dfb30f174e/01_raw_data
projects_data/FC-d645e6a2-c939-45aa-ae1e-35dfb30f174e/02_processed_data
projects_data/FC-d645e6a2-c939-45aa-ae1e-35dfb30f174e/03_reports
projects_data/FC-d94f4ae6-3be0-4822-8edd-60ac023288ce
projects_data/FC-d94f4ae6-3be0-4822-8edd-60ac023288ce/01_raw_data
projects_data/FC-d94f4ae6-3be0-4822-8edd-60ac023288ce/02_processed_data
projects_data/FC-d94f4ae6-3be0-4822-8edd-60ac023288ce/03_reports
projects_data/FC-da6829ef-5862-4c8d-9cff-32c397e0fe42
projects_data/FC-da6829ef-5862-4c8d-9cff-32c397e0fe42/01_raw_data
projects_data/FC-da6829ef-5862-4c8d-9cff-32c397e0fe42/02_processed_data
projects_data/FC-da6829ef-5862-4c8d-9cff-32c397e0fe42/03_reports
projects_data/FC-dac8fa4a-efb6-4720-838e-617dc1ae3433
projects_data/FC-dac8fa4a-efb6-4720-838e-617dc1ae3433/01_raw_data
projects_data/FC-dac8fa4a-efb6-4720-838e-617dc1ae3433/02_processed_data
projects_data/FC-dac8fa4a-efb6-4720-838e-617dc1ae3433/03_reports
projects_data/FC-dbc8c18c-fedc-49dc-9c36-f3423303b19b
projects_data/FC-dbc8c18c-fedc-49dc-9c36-f3423303b19b/01_raw_data
projects_data/FC-dbc8c18c-fedc-49dc-9c36-f3423303b19b/02_processed_data
projects_data/FC-dbc8c18c-fedc-49dc-9c36-f3423303b19b/03_reports
projects_data/FC-e06edf9d-459a-46f1-86c9-b43fa6599fb3
projects_data/FC-e06edf9d-459a-46f1-86c9-b43fa6599fb3/01_raw_data
projects_data/FC-e06edf9d-459a-46f1-86c9-b43fa6599fb3/02_processed_data
projects_data/FC-e06edf9d-459a-46f1-86c9-b43fa6599fb3/03_reports
projects_data/FC-e0c8a0c0-774d-4bf8-aeaf-5820c076f042
projects_data/FC-e0c8a0c0-774d-4bf8-aeaf-5820c076f042/01_raw_data
projects_data/FC-e0c8a0c0-774d-4bf8-aeaf-5820c076f042/02_processed_data
projects_data/FC-e0c8a0c0-774d-4bf8-aeaf-5820c076f042/03_reports
projects_data/FC-e138267f-f036-413d-a7ab-c14f7ac86b5e
projects_data/FC-e138267f-f036-413d-a7ab-c14f7ac86b5e/01_raw_data
projects_data/FC-e138267f-f036-413d-a7ab-c14f7ac86b5e/02_processed_data
projects_data/FC-e138267f-f036-413d-a7ab-c14f7ac86b5e/03_reports
projects_data/FC-e21b7947-5dc1-4ae7-bc07-f2bb3cf16339
projects_data/FC-e21b7947-5dc1-4ae7-bc07-f2bb3cf16339/01_raw_data
projects_data/FC-e21b7947-5dc1-4ae7-bc07-f2bb3cf16339/02_processed_data
projects_data/FC-e21b7947-5dc1-4ae7-bc07-f2bb3cf16339/03_reports
projects_data/FC-e2c78646-ee3a-4c0c-bc4d-3c5695e72b74
projects_data/FC-e2c78646-ee3a-4c0c-bc4d-3c5695e72b74/01_raw_data
projects_data/FC-e2c78646-ee3a-4c0c-bc4d-3c5695e72b74/02_processed_data
projects_data/FC-e2c78646-ee3a-4c0c-bc4d-3c5695e72b74/03_reports
projects_data/FC-e3a6573e-2264-4cba-837c-31a72b3abe2e
projects_data/FC-e3a6573e-2264-4cba-837c-31a72b3abe2e/01_raw_data
projects_data/FC-e3a6573e-2264-4cba-837c-31a72b3abe2e/02_processed_data
projects_data/FC-e3a6573e-2264-4cba-837c-31a72b3abe2e/03_reports
projects_data/FC-e4b4938d-96e1-4917-bdae-e0546ef2ef6f
projects_data/FC-e4b4938d-96e1-4917-bdae-e0546ef2ef6f/01_raw_data
projects_data/FC-e4b4938d-96e1-4917-bdae-e0546ef2ef6f/02_processed_data
projects_data/FC-e4b4938d-96e1-4917-bdae-e0546ef2ef6f/03_reports
projects_data/FC-e57a9013-99bc-498d-aacc-87c0bbc4062e
projects_data/FC-e57a9013-99bc-498d-aacc-87c0bbc4062e/01_raw_data
projects_data/FC-e57a9013-99bc-498d-aacc-87c0bbc4062e/02_processed_data
projects_data/FC-e57a9013-99bc-498d-aacc-87c0bbc4062e/03_reports
projects_data/FC-e819f387-b1f3-41f3-8892-d1c5f4fdd347
projects_data/FC-e819f387-b1f3-41f3-8892-d1c5f4fdd347/01_raw_data
projects_data/FC-e819f387-b1f3-41f3-8892-d1c5f4fdd347/02_processed_data
projects_data/FC-e819f387-b1f3-41f3-8892-d1c5f4fdd347/03_reports
projects_data/FC-e8a974e3-46fe-4301-b37a-3d7735445eb2
projects_data/FC-e8a974e3-46fe-4301-b37a-3d7735445eb2/01_raw_data
projects_data/FC-e8a974e3-46fe-4301-b37a-3d7735445eb2/02_processed_data
projects_data/FC-e8a974e3-46fe-4301-b37a-3d7735445eb2/03_reports
projects_data/FC-eb3ed65a-9de6-45cb-8273-d424b5c48427
projects_data/FC-eb3ed65a-9de6-45cb-8273-d424b5c48427/01_raw_data
projects_data/FC-eb3ed65a-9de6-45cb-8273-d424b5c48427/02_processed_data
projects_data/FC-eb3ed65a-9de6-45cb-8273-d424b5c48427/03_reports
projects_data/FC-ed14f398-8b2d-4a66-8502-477ef8bac6d8
projects_data/FC-ed14f398-8b2d-4a66-8502-477ef8bac6d8/01_raw_data
projects_data/FC-ed14f398-8b2d-4a66-8502-477ef8bac6d8/02_processed_data
projects_data/FC-ed14f398-8b2d-4a66-8502-477ef8bac6d8/03_reports
projects_data/FC-ed5b5772-504e-412c-b0e9-e8aae914b55b
projects_data/FC-ed5b5772-504e-412c-b0e9-e8aae914b55b/01_raw_data
projects_data/FC-ed5b5772-504e-412c-b0e9-e8aae914b55b/02_processed_data
projects_data/FC-ed5b5772-504e-412c-b0e9-e8aae914b55b/03_reports
projects_data/FC-f1289d43-1f36-4723-b464-87afa78eaeb8
projects_data/FC-f1289d43-1f36-4723-b464-87afa78eaeb8/01_raw_data
projects_data/FC-f1289d43-1f36-4723-b464-87afa78eaeb8/02_processed_data
projects_data/FC-f1289d43-1f36-4723-b464-87afa78eaeb8/03_reports
projects_data/FC-f157829c-3920-424c-8c43-e91026be4525
projects_data/FC-f157829c-3920-424c-8c43-e91026be4525/01_raw_data
projects_data/FC-f157829c-3920-424c-8c43-e91026be4525/02_processed_data
projects_data/FC-f157829c-3920-424c-8c43-e91026be4525/03_reports
projects_data/FC-f4afa954-b661-4200-a75f-4209b959120e
projects_data/FC-f4afa954-b661-4200-a75f-4209b959120e/01_raw_data
projects_data/FC-f4afa954-b661-4200-a75f-4209b959120e/02_processed_data
projects_data/FC-f4afa954-b661-4200-a75f-4209b959120e/03_reports
projects_data/FC-f8fe6026-18c1-4cc6-91ea-2b1166ca35c9
projects_data/FC-f8fe6026-18c1-4cc6-91ea-2b1166ca35c9/01_raw_data
projects_data/FC-f8fe6026-18c1-4cc6-91ea-2b1166ca35c9/02_processed_data
projects_data/FC-f8fe6026-18c1-4cc6-91ea-2b1166ca35c9/03_reports
projects_data/FC-f94065f1-9a23-44ec-a84d-a6d3b4031a1f
projects_data/FC-f94065f1-9a23-44ec-a84d-a6d3b4031a1f/01_raw_data
projects_data/FC-f94065f1-9a23-44ec-a84d-a6d3b4031a1f/02_processed_data
projects_data/FC-f94065f1-9a23-44ec-a84d-a6d3b4031a1f/03_reports
projects_data/FC-f9acc753-94af-4b70-a940-df69e390ba38
projects_data/FC-f9acc753-94af-4b70-a940-df69e390ba38/01_raw_data
projects_data/FC-f9acc753-94af-4b70-a940-df69e390ba38/02_processed_data
projects_data/FC-f9acc753-94af-4b70-a940-df69e390ba38/03_reports
projects_data/FC-fab07fa9-a589-4c73-96ef-3b64495b8e79
projects_data/FC-fab07fa9-a589-4c73-96ef-3b64495b8e79/01_raw_data
projects_data/FC-fab07fa9-a589-4c73-96ef-3b64495b8e79/02_processed_data
projects_data/FC-fab07fa9-a589-4c73-96ef-3b64495b8e79/03_reports
projects_data/FC-fc9afd6e-26cc-4154-a84f-241866fe82c1
projects_data/FC-fc9afd6e-26cc-4154-a84f-241866fe82c1/01_raw_data
projects_data/FC-fc9afd6e-26cc-4154-a84f-241866fe82c1/02_processed_data
projects_data/FC-fc9afd6e-26cc-4154-a84f-241866fe82c1/03_reports
projects_data/FC-fcf02e2e-98f5-4f7c-bd5f-0e21e15b39c8
projects_data/FC-fcf02e2e-98f5-4f7c-bd5f-0e21e15b39c8/01_raw_data
projects_data/FC-fcf02e2e-98f5-4f7c-bd5f-0e21e15b39c8/02_processed_data
projects_data/FC-fcf02e2e-98f5-4f7c-bd5f-0e21e15b39c8/03_reports
projects_data/FC-fd9ef45b-9178-48f1-80bc-1a7a37de859d
projects_data/FC-fd9ef45b-9178-48f1-80bc-1a7a37de859d/01_raw_data
projects_data/FC-fd9ef45b-9178-48f1-80bc-1a7a37de859d/02_processed_data
projects_data/FC-fd9ef45b-9178-48f1-80bc-1a7a37de859d/03_reports
projects_data/FC-fdaf3c44-89c0-407a-8232-afa5bd82d39c
projects_data/FC-fdaf3c44-89c0-407a-8232-afa5bd82d39c/01_raw_data
projects_data/FC-fdaf3c44-89c0-407a-8232-afa5bd82d39c/02_processed_data
projects_data/FC-fdaf3c44-89c0-407a-8232-afa5bd82d39c/03_reports
projects_data/TEST-JOB-123
projects_data/TEST-JOB-123/01_raw_data
projects_data/TEST-JOB-123/02_processed_data
projects_data/TEST-JOB-123/03_reports
pyproject.toml
pytest.ini
README.md
requirements.txt
scripts
scripts/gen-mqtt-cert.sh
scripts/make_audit_bundle.sh
scripts/make_full_audit.py
scripts/no_bom_check.py
scripts/remove_bom.py
test.db
tests
tests/conftest.py
tests/test_api.py
tests/test_archivist.py
tests/test_pagination.py
tls.crt
tls.key
```

---

## File Contents

### Dockerfile

```
FROM python:3.11-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# include Alembic bits so the container knows where migrations live
COPY alembic.ini .
COPY migrations ./migrations

COPY ./app ./app

CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000

```



### docker-compose.yml

```
# docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    env_file: .env
    ports: [ "${DB_PORT:-5432}:5432" ]
    volumes: [ pgdata:/var/lib/postgresql/data ]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # THIS IS THE MISSING SERVICE
  mosquitto:
    image: eclipse-mosquitto:2
    restart: unless-stopped
    ports:
      - "1883:1883"
      - "8883:8883"
    volumes:
      - ./mosquitto/conf:/mosquitto/config
      - ./mosquitto/certs:/mosquitto/certs
      - mosquitto_data:/mosquitto/data

  eventbus:
    build: .
    restart: unless-stopped
    env_file: .env
    ports: [ "8000:8000" ]
    volumes: [ ./projects_data:/code/projects_data ]
    depends_on:
      postgres:  { condition: service_healthy }
      mosquitto: { condition: service_started }

volumes:
  pgdata:
  mosquitto_data: # Add this volume for mosquitto
```



### alembic.ini

```
# A generic, single database configuration.

[alembic]
# path to migration scripts.
# this is typically a path given in POSIX (e.g. forward slashes)
# format, relative to the token %(here)s which refers to the location of this
# ini file
script_location = migrations

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.  for multiple paths, the path separator
# is defined by "path_separator" below.
prepend_sys_path = .


# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python>=3.9 or backports.zoneinfo library and tzdata library.
# Any required deps can installed by adding `alembic[tz]` to the pip requirements
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to <script_location>/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "path_separator"
# below.
# version_locations = %(here)s/bar:%(here)s/bat:%(here)s/alembic/versions

# path_separator; This indicates what character is used to split lists of file
# paths, including version_locations and prepend_sys_path within configparser
# files such as alembic.ini.
# The default rendered in new alembic.ini files is "os", which uses os.pathsep
# to provide os-dependent path splitting.
#
# Note that in order to support legacy alembic.ini files, this default does NOT
# take place if path_separator is not present in alembic.ini.  If this
# option is omitted entirely, fallback logic is as follows:
#
# 1. Parsing of the version_locations option falls back to using the legacy
#    "version_path_separator" key, which if absent then falls back to the legacy
#    behavior of splitting on spaces and/or commas.
# 2. Parsing of the prepend_sys_path option falls back to the legacy
#    behavior of splitting on spaces, commas, or colons.
#
# Valid values for path_separator are:
#
# path_separator = :
# path_separator = ;
# path_separator = space
# path_separator = newline
#
# Use os.pathsep. Default configuration used for new projects.
path_separator = os

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

# database URL.  This is consumed by the user-maintained env.py script only.
# other means of configuring database URLs may be customized within the env.py
# file.
sqlalchemy.url = ${DATABASE_URL}



[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the module runner, against the "ruff" module
# hooks = ruff
# ruff.type = module
# ruff.module = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Alternatively, use the exec runner to execute a binary found on your PATH
# hooks = ruff
# ruff.type = exec
# ruff.executable = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Logging configuration.  This is also consumed by the user-maintained
# env.py script only.
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

```



### pyproject.toml

```
# pyproject.toml

[tool.black]
line-length = 88
target-version = ["py311"]
# Optional (locks version so CI & local stay identical):
# required-version = "25.1.0"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I"]

# (Optional) add ignores or per-file-ignores here later.

[tool.ruff.format]
# Only put *formatting* options here if you customize them.
# For now we leave it empty so Ruff uses defaults
# (indent-style, quote-style, etc. not needed unless you want custom behavior).

```



### requirements.txt

```
# =========================
# Aegis Event Bus – Requirements
# =========================
# Strategy:
# - Pin to compatible minor ranges using ~= so you get bug fixes but not breaking major jumps.
# - Testing & dev tools live here for simplicity (can later split into prod/dev files).

# --- Core Framework ---
fastapi~=0.111.0
uvicorn[standard]~=0.30.0
python-dotenv~=1.0.0
structlog~=24.1.0
typer~=0.12.0

# --- Database & ORM ---
sqlmodel~=0.0.22
alembic~=1.13.0
asyncpg~=0.29.0
psycopg2-binary~=2.9.0

# --- Security & Auth ---
bcrypt>=4.1.2,<5
passlib[bcrypt]~=1.7.4
python-jose[cryptography]~=3.3.0
python-multipart~=0.0.9

# --- Event Messaging ---
paho-mqtt~=2.1.0

# --- Observability ---
prometheus-fastapi-instrumentator~=7.0.0

# --- Testing ---
pytest~=8.4.0
httpx~=0.27.0


```



### .pre-commit-config.yaml

```
repos:
  - repo: https://github.com/psf/black
    rev: 25.1.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.10
    hooks:
      - id: ruff
        args: [--fix]

  - repo: local
    hooks:
      - id: no-bom
        name: Ensure requirements.txt has no UTF-8 BOM
        language: system
        entry: python scripts/no_bom_check.py
        pass_filenames: false
        files: ^requirements\.txt$

```



### README.md

```
# Aegis Event-Bus (Agent A0) · v0.1

This is the secure, auditable, and scalable backbone for the Aegis Multi-Agent AI ecosystem. It is designed to handle job requests, manage data, and emit events for other agents to consume.

---
## Features

- **FastAPI Service:** Provides a modern, asynchronous API for job management.
- **JWT Authentication:** Endpoints are secured, requiring a valid token for access.
- **SQLite Backend:** Simple, file-based, and reliable data persistence.
- **Automated Folder Creation:** Creates a standardized directory structure for each new job.
- **MQTT Event Publishing:** Broadcasts a `job.created` event for other agents.
- **Containerized:** Runs entirely within Docker via a simple `docker-compose` command.
- **Automated Testing:** Includes a full suite of unit tests with `pytest` and automated CI via GitHub Actions.

---

## Prerequisites

| Tool           | Notes                          |
| -------------- | ------------------------------ |
| Python         | 3.11+                          |
| Docker         | Latest version                 |
| Docker Compose | Latest version (usually incl. with Docker) |

---

## 🚀 Quick Start (Using Docker Compose)

This is the recommended way to run the application.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/aegis-event-bus.git](https://github.com/your-username/aegis-event-bus.git)
    cd aegis-event-bus
    ```

2.  **Configure Environment:**
    Copy the example environment file. No changes are needed for default local startup.
    ```bash
    cp .env.example .env
    ```

3.  **Run the Application Stack:**
    This single command will build and start the FastAPI service and the MQTT broker.
    ```bash
    docker compose up --build
    ```

---

## Accessing the Services

- **API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **MQTT Broker:** `localhost:1883`

---

## 🧪 Running Tests

1.  Create and activate a Python virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
2.  Install dependencies.
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the test suite.
    ```bash
    pytest -v
    ```
    ---
## Advanced Usage

### Pagination

The `GET /jobs` endpoint supports cursor-based pagination.

`GET /jobs?limit=20&cursor=<last_id>`

This will return a JSON object with `items` and a `next_cursor`. To fetch the next page, make the same request again, passing the received `next_cursor` value in the `cursor` query parameter.

### Generate an Admin JWT

You can generate a long-lived token for administrative or testing purposes using the built-in CLI.

```bash
python -m app.cli create-token admin --minutes 1440
```



### app/main.py

```
# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from . import db, endpoints, logging_config, security

# ---------- logging & metrics set‑up ----------
logging_config.setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()  # creates tables when running under pytest (SQLite)
    yield


# ---------------------------------------------

app = FastAPI(title="Aegis Event Bus", lifespan=lifespan)

Instrumentator().instrument(app).expose(app, include_in_schema=False)

app.include_router(endpoints.router)
app.include_router(security.router)

```



### app/db.py

```
# app/db.py
import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite:///eventbus.db")
IS_SQLITE = DB_URL.startswith("sqlite")

engine = create_engine(
    DB_URL,
    echo=False,
    connect_args={"check_same_thread": False} if IS_SQLITE else {},
)


def init_db() -> None:
    """Create tables only for SQLite.  In Postgres we rely on Alembic."""
    if IS_SQLITE:
        SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

```



### app/endpoints.py

```
# app/endpoints.py
import json
import os
from uuid import uuid4

import paho.mqtt.publish as mqtt_publish
import structlog
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, text

from . import archivist, schemas, security
from .db import get_session
from .models import AuditLog

router = APIRouter()
log = structlog.get_logger(__name__)

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))


@router.get("/healthz", include_in_schema=False)
def health_check(session: Session = Depends(get_session)):
    """A simple health check endpoint that pings the database."""
    session.exec(text("SELECT 1"))
    return {"status": "ok"}


@router.get("/", tags=["Status"])
def read_root():
    return {"status": "Aegis Event Bus is online"}


@router.post("/job", response_model=schemas.Job, tags=["Jobs"])
def create_new_job(
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    job_id = f"FC-{uuid4()}"
    archivist.create_job_folders(job_id, archivist.DATA_ROOT)

    with session:
        entry = AuditLog(job_id=job_id, action="job.created")
        session.add(entry)
        session.commit()
        session.refresh(entry)

    payload = {"job_id": job_id, "timestamp": entry.timestamp.isoformat()}
    try:
        mqtt_publish.single(
            topic="aegis/job/created",
            payload=json.dumps(payload),
            hostname=MQTT_HOST,
            port=MQTT_PORT,
            tls={"ca_certs": "./mosquitto/certs/ca.crt"},
        )
    except Exception as exc:
        log.warning("mqtt.publish_failed", job_id=job_id, err=str(exc))

    return {"job_id": job_id}


@router.get("/jobs", response_model=schemas.JobsPage, tags=["Jobs"])
def list_recent_jobs(
    session: Session = Depends(get_session),
    cursor: int | None = Query(None, description="last row id from prev page"),
    limit: int = Query(20, le=100),
    _: dict = Depends(security.get_current_user),
):
    stmt = select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)
    if cursor:
        stmt = stmt.where(AuditLog.id < cursor)

    rows = session.exec(stmt).all()

    next_cursor = rows[-1].id if len(rows) == limit else None
    return {"items": rows, "next_cursor": next_cursor}

```



### app/security.py

```
# app/security.py
import os

# This is the key fix: importing timedelta directly from the datetime module
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import schemas

load_dotenv()
router = APIRouter()

# --- Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "a_default_secret_key_for_testing")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Fake User Database ---
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": pwd_context.hash("testpassword"),
    }
}


def get_user(username: str):
    return fake_users_db.get(username)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- The Main Security Dependency ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # This now works because timedelta was imported correctly
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

```



### app/schemas.py

```
# app/schemas.py
from typing import List, Optional

from pydantic import BaseModel

from .models import AuditLog


class Job(BaseModel):
    job_id: str


class Token(BaseModel):
    access_token: str
    token_type: str


class JobsPage(BaseModel):
    items: List[AuditLog]
    next_cursor: Optional[int] = None

```



### app/logging_config.py

```
# app/logging_config.py
import logging
import sys

import structlog
from structlog.processors import JSONRenderer, TimeStamper


def setup_logging() -> None:
    """One‑shot Structlog configuration for the whole service."""
    timestamper = TimeStamper(fmt="iso", utc=True)

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
        processors=[
            structlog.contextvars.merge_contextvars,  # request‑id etc.
            structlog.processors.add_log_level,
            timestamper,
            structlog.processors.dict_tracebacks,  # pretty tracebacks
            JSONRenderer(),  # final JSON out
        ],
    )

    # The std‑lib side; structlog will feed into this.
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",  # structlog already produced JSON
        stream=sys.stdout,
    )

```



### app/cli.py

```
# app/cli.py
import datetime as dt
import os

import typer
from dotenv import load_dotenv
from jose import jwt

load_dotenv()
app = typer.Typer()

SECRET = os.getenv("SECRET_KEY")
ALG = os.getenv("ALGORITHM", "HS256")


@app.command(help="Generate a short-lived admin JWT")
def create_token(username: str, minutes: int = 60):
    """Generates a JWT for the given username, valid for a number of minutes."""
    exp = dt.datetime.utcnow() + dt.timedelta(minutes=minutes)
    token = jwt.encode({"sub": username, "exp": exp}, SECRET, algorithm=ALG)
    typer.echo(f"Generated token for user '{username}':")
    typer.echo(token)


if __name__ == "__main__":
    app()

```



### app/archivist.py

```
# app/archivist.py
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# We still define DATA_ROOT here to be used by the main application
DATA_ROOT = Path(os.getenv("DATA_ROOT", "projects_data"))


def create_job_folders(job_id: str, base_path: Path):
    """
    Creates the standard folder structure for a new job inside a given base_path.
    """
    job_root = base_path / job_id
    subfolders = ["01_raw_data", "02_processed_data", "03_reports"]

    # Ensure the main data root directory exists
    base_path.mkdir(exist_ok=True)

    for sub in subfolders:
        (job_root / sub).mkdir(parents=True, exist_ok=True)

```



### app/models.py

```
# app/models.py
import datetime as dt
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: str = Field(index=True)
    action: str
    timestamp: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

```



### migrations/env.py

```
"""
Alembic migration environment.
Keeps DATABASE_URL in sync with .env and exposes SQLModel metadata.
"""

import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

load_dotenv()  # .env → env vars
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL not set")

# ——— Alembic config ————————————————————————————————————————————
config = context.config
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name:
    fileConfig(config.config_file_name)

# ——— Import models so Alembic can autogenerate ————————————
from sqlmodel import SQLModel  # noqa: E402

target_metadata = SQLModel.metadata
# ——————————————————————————————————————————————————————————————


def run_migrations_offline() -> None:
    """Run migrations without a DB connection (generates SQL)."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a live DB connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```



### migrations/versions
#### migrations\versions\__pycache__\bd536313df34_create_audit_log.cpython-313.pyc

```
[BINARY or NON-UTF8: bd536313df34_create_audit_log.cpython-313.pyc]
```

#### migrations\versions\bd536313df34_create_audit_log.py

```
"""create audit_log

Revision ID: bd536313df34
Revises:
Create Date: 2025-07-13 22:18:24.110812

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "bd536313df34"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_auditlog_job_id"), table_name="auditlog")
    op.drop_table("auditlog")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auditlog",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("job_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("action", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "timestamp",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("auditlog_pkey")),
    )
    op.create_index(op.f("ix_auditlog_job_id"), "auditlog", ["job_id"], unique=False)
    # ### end Alembic commands ###

```



### tests/conftest.py

```
# tests/conftest.py
"""
Pytest fixtures for the Event Bus service.

We intentionally set DATABASE_URL *before* importing `app.db` so the
application uses an in‑memory SQLite engine during tests.

Ruff rule E402 (imports not at top) is suppressed because of this one
required assignment.
"""

# ruff: noqa: E402

import os

# Must be set before importing app.db so its engine points to SQLite memory.
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import app.db as db
from app.main import app

# ---------- shared in-memory engine ----------
engine = create_engine(
    "sqlite://",  # single in-memory DB
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # one global connection so tables persist across sessions
)
db.engine = engine  # make the app use this engine
# ---------------------------------------------


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Override dependency to always return our shared session
    db.get_session = lambda: session
    yield TestClient(app)

```



### tests/test_api.py

```
# tests/test_api.py
"""
API integration tests (synchronous) for the Event Bus service.

Key policy:
-----------
All external side‑effects (MQTT publish) are mocked so the test
suite never opens network connections on CI (important for
GitHub Actions ToS compliance and speed).

We rely on fixtures from tests/conftest.py:
- client  : FastAPI TestClient
- session : SQLModel Session bound to the test DB
"""

import paho.mqtt.publish as mqtt_publish
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import AuditLog


# ────────────────────────── GLOBAL MQTT MOCK ──────────────────────────
@pytest.fixture(autouse=True)
def _mock_mqtt(monkeypatch):
    """
    Auto‑applied fixture that replaces paho.mqtt.publish.single with a no‑op.

    This guarantees **zero network traffic** for every test, even if a
    future test forgets to monkeypatch explicitly.
    """
    monkeypatch.setattr(mqtt_publish, "single", lambda *a, **k: None)


# ───────────────────────────── TESTS ──────────────────────────────────
def test_read_root_endpoint(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "Aegis Event Bus is online"}


def test_unauthenticated_routes(client: TestClient):
    # POST /job without token
    assert client.post("/job").status_code == 401
    # GET /jobs without token
    assert client.get("/jobs").status_code == 401


def test_auth_and_workflow(client: TestClient, session: Session):
    # 1. Obtain JWT
    token = client.post(
        "/token", data={"username": "testuser", "password": "testpassword"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a job (MQTT publish is silently mocked)
    job_id = client.post("/job", headers=headers).json()["job_id"]

    # 3. Verify DB row
    db_row = session.exec(select(AuditLog).where(AuditLog.job_id == job_id)).one()
    assert db_row.action == "job.created"

    # 4. List jobs & confirm first returned matches
    jobs_page = client.get("/jobs", headers=headers).json()
    assert jobs_page["items"][0]["job_id"] == job_id

```



### tests/test_pagination.py

```
# tests/test_pagination.py
import paho.mqtt.publish as mqtt_publish
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.models import AuditLog


def _login_and_get_headers(client: TestClient):
    """Helper function to log in and get auth headers."""
    data = {"username": "testuser", "password": "testpassword"}
    token = client.post("/token", data=data).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_jobs_pagination(client: TestClient, session: Session, monkeypatch):
    """Tests that the /jobs endpoint correctly paginates results."""
    headers = _login_and_get_headers(client)
    monkeypatch.setattr(mqtt_publish, "single", lambda *a, **k: None)

    # Clean the DB and create 3 new jobs
    session.exec(delete(AuditLog))
    session.commit()
    for _ in range(3):
        client.post("/job", headers=headers)

    # --- Test First Page ---
    page1_response = client.get("/jobs?limit=2", headers=headers)
    assert page1_response.status_code == 200
    page1 = page1_response.json()

    assert len(page1["items"]) == 2
    assert page1["next_cursor"] is not None
    assert page1["items"][0]["id"] == 3  # Should be the newest job
    assert page1["items"][1]["id"] == 2

    # --- Test Second Page ---
    cursor = page1["next_cursor"]
    page2_response = client.get(f"/jobs?limit=2&cursor={cursor}", headers=headers)
    assert page2_response.status_code == 200
    page2 = page2_response.json()

    assert len(page2["items"]) == 1  # Only one job left
    assert page2["next_cursor"] is None  # Should be the last page
    assert page2["items"][0]["id"] == 1

```



### tests/test_archivist.py

```
# tests/test_archivist.py

import shutil
from pathlib import Path

from app.archivist import create_job_folders

# Define a temporary folder name for our tests to use
TEST_DATA_ROOT = Path("test_projects_data_temp")


def test_folder_creation():
    """
    Tests if the create_job_folders function correctly creates the
    required directory structure.
    """
    job_id = "TEST-JOB-123"

    # --- Run the function we are testing, providing the base_path ---
    create_job_folders(job_id=job_id, base_path=TEST_DATA_ROOT)

    # --- Assert that the folders now exist ---
    assert (TEST_DATA_ROOT / job_id).is_dir()
    assert (TEST_DATA_ROOT / job_id / "01_raw_data").is_dir()

    # --- Clean up after the test is done ---
    shutil.rmtree(TEST_DATA_ROOT)

```



### scripts/gen-mqtt-cert.sh

```
#!/usr/bin/env bash
set -e
mkdir -p mosquitto/certs
mkdir -p mosquitto/conf

# Root CA
# The //CN=... is the fix for Git Bash on Windows
openssl req -x509 -nodes -days 3650 \
  -newkey rsa:2048 \
  -keyout mosquitto/certs/ca.key \
  -out  mosquitto/certs/ca.crt \
  -subj "//CN=AegisDevCA"

# Server cert
# The //CN=... is the fix for Git Bash on Windows
openssl req -nodes -newkey rsa:2048 \
  -keyout mosquitto/certs/server.key \
  -out  mosquitto/certs/server.csr \
  -subj "//CN=mosquitto"

openssl x509 -req -days 3650 \
  -in  mosquitto/certs/server.csr \
  -CA  mosquitto/certs/ca.crt \
  -CAkey mosquitto/certs/ca.key -CAcreateserial \
  -out mosquitto/certs/server.crt

echo "TLS certs generated in mosquitto/certs/"
```


