{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    python311Packages.pip
    stdenv.cc.cc.lib
    zlib
    gh
  ];
  shellHook = ''
    export LD_LIBRARY_PATH="${
      pkgs.lib.makeLibraryPath [
        pkgs.stdenv.cc.cc.lib
        pkgs.zlib
      ]
    }:$LD_LIBRARY_PATH"
        python -m venv .venv
        source .venv/bin/activate
        pip install streamlit cvd-risk
        echo "Run 'streamlit run app.py' to start the qrisk3 calculator."
  '';
}
