package = "botwar"
version = "0.1-0"

source = {
  url = "git://github.com/spacebeam/starcraft-scif",
  tag = "0.1.0",
}

description = {
  summary = "",
  detailed = "",
  homepage = "",
  license = ""
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
    ['bw.version'] = "src/version.lua" 
  },
  install = {
    bin = {
      ['bw'] = "src/bw.lua"
    }
  }
}
