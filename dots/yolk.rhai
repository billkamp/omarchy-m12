export let eggs = #{
    home: #{
        targets: #{
            ".config/hypr/looknfeel.lua": "~/.config/hypr/looknfeel.lua",
            ".config/hypr/bindings.lua": "~/.config/hypr/bindings.lua",
        },
        unsafe_shell_hooks: #{
            pre_deploy: "bash \"$HOME/.config/yolk/hooks/prepare-hypr.sh\"",
            post_deploy: "bash \"$HOME/.config/yolk/hooks/apply-bashrc.sh\"",
        },
    },
};
