[app]

title = SLA Tickets
package.name = slatickets
package.domain = org.sla

source.dir = .
source.include_exts = py,xlsx,png,ico

version = 1.0

requirements = python3,kivy,pandas,openpyxl

orientation = portrait

fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21

[buildozer]

log_level = 2
warn_on_root = 1