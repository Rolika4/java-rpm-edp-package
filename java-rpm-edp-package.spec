%global source_date_epoch_from_changelog 0
%define debug_package %{nil}

%if 0%{?RELEASE_NUMBER:1} != 0
%define rel %{?RELEASE_NUMBER}
%else
%define rel 1
%endif

%if 0%{?VERSION_NUMBER:1} != 0
%define ver %{?VERSION_NUMBER}
%else
%define ver 0.1.0
%endif

Name:           java-rpm-edp-package
Version:        %{ver}
Release:        %{rel}
Summary:        java-rpm-edp-package application
ExclusiveArch:  %{_arch}

License:        Apache-2.0
URL:            https://github.com/epmd-edp/java-maven-java11.git
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.service

Requires:       bash
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
java-rpm-edp-package application

%prep
%setup -q

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
install -m 0755 %{name} %{buildroot}/%{_bindir}/%{name}

# Install the systemd service file
install -D -m 0644 %{SOURCE1} %{buildroot}/etc/systemd/system/%{name}.service

%post
# Reload systemd daemon and enable the service
systemctl daemon-reload
systemctl enable %{name}.service
systemctl start %{name}.service

%preun
# Stop and disable the service before uninstall
systemctl stop %{name}.service
systemctl disable %{name}.service

%postun
# Reload systemd daemon after uninstall
systemctl daemon-reload

%files
%{_bindir}/%{name}
%config(noreplace) /etc/systemd/system/%{name}.service
