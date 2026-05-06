[app]
title = SLA Tickets
package.name = slatickets
package.domain = org.randy
source.dir = .
source.include_exts = py,png,jpg,kv,xlsx
source.include_patterns = perimetro_mayo.xlsx
version = 1.0

requirements = python3,kivy,pandas,openpyxl

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
