{
  description = "wpa_supplicant";
  inputs.nixpkgs.url = "github:nixos/nixpkgs";

  outputs = { self, nixpkgs }: let
    supportedSystems = [ "x86_64-linux" ];
    forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
  in {
    packages = forAllSystems (system: with nixpkgs.legacyPackages.${system}; rec {
      wpa_supplicant = callPackage ./wpa_supplicant.nix { };
      default = wpa_supplicant;
    });
    devShells = forAllSystems (system: with nixpkgs.legacyPackages.${system}; rec {
      eiwd = mkShell {
        name = "wpa_supplicant-dev-shell";
        inputsFrom = [ self.packages.${system}.wpa_supplicant ];
      };
      default = wpa_supplicant;
    });
  };
}
