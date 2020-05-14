# Generated by Django 3.0.3 on 2020-04-10 15:49

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImpactedPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Importer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the importer', max_length=100, unique=True)),
                ('license', models.CharField(blank=True, help_text='License of the vulnerability data', max_length=100)),
                ('last_run', models.DateTimeField(help_text='UTC Timestamp of the last run', null=True)),
                ('data_source', models.CharField(help_text='Class name of the data source implementation importable from vulnerabilities.importers', max_length=100)),
                ('data_source_cfg', django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='Implementation-specific configuration for the data source')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, help_text='A short code to identify the type of this package. For example: gem for a Rubygem, docker for a container, pypi for a Python Wheel or Egg, maven for a Maven Jar, deb for a Debian package, etc.', max_length=16, null=True)),
                ('namespace', models.CharField(blank=True, help_text='Package name prefix, such as Maven groupid, Docker image owner, GitHub user or organization, etc.', max_length=255, null=True)),
                ('name', models.CharField(blank=True, help_text='Name of the package.', max_length=100, null=True)),
                ('version', models.CharField(blank=True, help_text='Version of the package.', max_length=50, null=True)),
                ('qualifiers', models.CharField(blank=True, help_text='Extra qualifying data for a package such as the name of an OS, architecture, distro, etc.', max_length=1024, null=True)),
                ('subpath', models.CharField(blank=True, help_text='Extra subpath within a package, relative to the package root.', max_length=200, null=True)),
            ],
            options={
                  'unique_together': {('name', 'namespace', 'type', 'version', 'qualifiers', 'subpath')},
                  'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cve_id', models.CharField(help_text='CVE ID', max_length=50, null=True, unique=True)),
                ('summary', models.TextField(blank=True, help_text='Summary of the vulnerability')),
                ('cvss', models.FloatField(help_text='CVSS Score', max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Vulnerabilities',
            },
        ),
        migrations.CreateModel(
            name='ResolvedPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vulnerabilities.Package')),
                ('vulnerability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vulnerabilities.Vulnerability')),
            ],
        ),
        migrations.AddField(
            model_name='package',
            name='vulnerabilities',
            field=models.ManyToManyField(through='vulnerabilities.ImpactedPackage', to='vulnerabilities.Vulnerability'),
        ),
        migrations.AddField(
            model_name='impactedpackage',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vulnerabilities.Package'),
        ),
        migrations.AddField(
            model_name='impactedpackage',
            name='vulnerability',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vulnerabilities.Vulnerability'),
        ),
        migrations.CreateModel(
            name='VulnerabilityReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, help_text='Source(s) name eg:NVD', max_length=50)),
                ('reference_id', models.CharField(blank=True, help_text='Reference ID, eg:DSA-4465-1', max_length=50)),
                ('url', models.URLField(blank=True, help_text='URL of Vulnerability data', max_length=1024)),
                ('vulnerability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vulnerabilities.Vulnerability')),
            ],
            options={
                'unique_together': {('vulnerability', 'source', 'reference_id', 'url')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='impactedpackage',
            unique_together={('vulnerability', 'package')},
        ),
    ]
