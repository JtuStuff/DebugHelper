use ipnetwork::IpNetwork;
use std::process;
use std::process::Command;
use clap::Parser;
use std::path::Path;
use std::net::{IpAddr, SocketAddr, TcpStream};
use std::time::Duration;
use serde::{Deserialize, Serialize};
use std::io::Read;

#[derive(Serialize, Deserialize, Parser, Debug)]
#[command(name = "DebugHelper")]
#[command(about = "A debug helper for the dmesg via ssh")]
#[command(bin_name = "debug_helper")]
#[command(author = "LatestOfMyMind || Orangeskai")]
#[command(version = "0.1.0")]

struct Args {
    /// Initialize the config
    #[arg(short, long)]
    init: bool,

    /// Force the app to run
    #[arg(short, long)]
    force: bool,
}

struct Config {
    username: String,
    password: String,
    hosting: String,
    last_interface: String,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            username: String::from(""),
            password: String::from(""),
            hosting: String::from(""),
            last_interface: String::from(""),
        }
    }
}

fn connect_to_port(target:IpAddr, port: u16) -> bool {
    let socket_address = SocketAddr::new(target, port);
    let timeout = Duration::from_millis(1);
    match TcpStream::connect_timeout(&socket_address, timeout) {
        Ok(_) => return true,
        Err(_) => return false,
    };
}

fn main() {
    let path = confy::get_configuration_file_path("debug_helper", "config").unwrap();
    let args = Args::parse();

    // Checking the os and force
    if cfg!(target_os = "windows") && !args.force {
        Command::new("cls").status().unwrap();
        println!("This app is not supported on windows");
        process::exit(1);
    } else {
        Command::new("clear").status().unwrap();
    }
    
    if args.init {
        println!("Initializing the config");
        // if the config file exists, ask if the user wants to overwrite it
        // if the config file doesn't exist, create it
        if Path::new(&path).exists() {
            println!("Config file already exists, do you want to overwrite it? [y/N]");
            let mut input = String::new();
            std::io::stdin().read_line(&mut input).unwrap();
            if input.trim().to_lowercase() == "y" {
                // confy::store("debug_helper", Config::default()).unwrap();
                println!("Config file created");
                process::exit(0);
            } else {
                println!("Config file not created");
                process::exit(0);
            }
        } else {
            // Initialize the struct
            let mut username = String::new();
            let mut password = String::new();
            let mut hosting = String::new();

            // Get the username
            println!("Please enter your username");
            std::io::stdin().read_line(&mut username).unwrap();
            username = username.trim().to_string();

            // Get the password
            println!("Please enter your password");
            std::io::stdin().read_line(&mut password).unwrap();
            password = password.trim().to_string();

            // Get the hosting
            println!("Please enter the hosting Default: https://0x0.st/");
            std::io::stdin().read_line(&mut hosting).unwrap();
            hosting = hosting.trim().to_string();
            if hosting == "" {
                hosting = String::from("https://0x0.st/");
            }
            
            println!("Username: {}", username);
            println!("Password: {}", username);
            println!("Hosting: {}", hosting);

            // confy::store("debug_helper", Config::default()).unwrap();
            println!("Config file created");
            // process::exit(0);
        }

    }

    if !Path::new(&path).exists() {
        println!("Config file doesn't exist, please run the app with --init");
        process::exit(1);
    }

    // let subnet = IpNetwork::new(IpAddr::V4(std::net::Ipv4Addr::new(192, 168, 1, 0)), 24).unwrap();
    // for ip in subnet.iter() {
    //     println!("Scanning {}", ip);
    //     if connect_to_port(ip, 22) {
    //         println!("{}:22 is open", ip);
    //         process::exit(0);
    //     }
    // }

}