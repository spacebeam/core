package = "bw"
version = "0.1-0"

source = {
  url = "git://github.com/spacebeam/starcraft-sif",
  tag = "0.1.0",
}

description = {
  summary = "bw command line toolkit",
  detailed = "It can download and launch Win32 C++ and Java bots " ..
  "or any Linux® bot with support for BWAPI 4.1.2, 4.2.0, 4.4.0.",
  homepage = "https://github.com/spacebeam",
  license = "AGPL3"
}

dependencies = {
  "lua == 5.1",
  "argparse",
  "luasocket",
  "uuid"
}

build = {
  type = 'builtin',
  modules = {
    ['bw.version'] = "src/version.lua",
    ['bw.tools'] = "src/tools.lua",
    ['bw.bots'] = "src/bots.lua"
  },
  install = {
    bin = {
      ['bw'] = "src/main.lua"
    }
  }
}
