use ipnetwork::IpNetwork;
use std::process;
use std::process::Command;
use clap::Parser;
use std::path::Path;
use pnet::datalink;
use std::net::{IpAddr, SocketAddr, TcpStream};
use std::time::Duration;
use serde::{Deserialize, Serialize};
use std::io::Read;
use ssh2::Session;


// ADD HANDLER IF THE INTERFACE IS NOT KNOWN
// ADD HANDLER IF Not found open port 22
// ADD VERBOSE

// REMOVE THE wlp1s0
const KNOWN_INTERFACES: [&str; 2] = ["rndis0", "usb0"];

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

#[derive(Serialize, Deserialize)]
struct Config {
    username: String,
    password: String,
    hosting: String,
    last_interface: String,
    fallback_interface: String,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            username: String::from(""),
            password: String::from(""),
            hosting: String::from(""),
            last_interface: String::from(""),
            fallback_interface: String::from(""),
        }
    }
}

fn run_ssh_command(session: &mut Session, command: &str) -> String {
    // Open a channel
    let mut channel = session.channel_session().unwrap();
    channel.exec(command).unwrap();

    // Read the output
    let mut result = String::new();
    channel.read_to_string(&mut result).unwrap();

    // Close the channel
    channel.close().unwrap();

    // Return the result
    result
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
                // Initialize the struct
                let mut username = String::new();
                let mut password = String::new();
                let mut hosting = String::new();
                let mut fallback_interface = String::new();

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

                // Get the fallback interface example wifi interface
                println!("Please enter the fallback interface Default: wlp1s0");
                std::io::stdin().read_line(&mut fallback_interface).unwrap();
                fallback_interface = fallback_interface.trim().to_string();
                if fallback_interface == "" {
                    fallback_interface = String::from("");
                }

                // write the config file
                confy::store("debug_helper", "config", Config {
                    username: username,
                    password: password,
                    hosting: hosting,
                    last_interface: String::from(""),
                    fallback_interface: fallback_interface,
                }).unwrap(); 

                println!("Config file created");
                process::exit(0);
                } else {
                    println!("Config file not being overwritten");
                    process::exit(0);
                }
        } else {
            // Initialize the struct
            let mut username = String::new();
            let mut password = String::new();
            let mut hosting = String::new();
            let mut fallback_interface = String::new();

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

            // Get the fallback interface example wifi interface
            println!("Please enter the fallback interface Default: wlp1s0");
            std::io::stdin().read_line(&mut fallback_interface).unwrap();
            fallback_interface = fallback_interface.trim().to_string();

            // write the config file
            confy::store("debug_helper", "config", Config {
                username: username,
                password: password,
                hosting: hosting,
                last_interface: String::from(""),
                fallback_interface: fallback_interface,
            }).unwrap(); 

            println!("Config file created");
            process::exit(0);
        }

    }

    if !Path::new(&path).exists() {
        println!("Config file doesn't exist, please run the app with --init");
        process::exit(1);
    }

    // load the config file
    let config: Config = confy::load("debug_helper", "config").unwrap();
 
    let interfaces = datalink::interfaces();

    let interface = if config.last_interface != "" {
        // try using last_interface first
        interfaces
            .iter()
            .find(|iface| iface.name == config.last_interface)
            .or_else(|| {
                // try using fallback_interface if last_interface is not found
                println!("Warning: Interface '{}' not found, trying fallback_interface...", config.last_interface);
                interfaces
                    .iter()
                    .find(|iface| iface.name == config.fallback_interface)
            })
            .or_else(|| {
                // try using known_interfaces if fallback_interface is not found
                println!("Warning: Fallback interface '{}' not found, trying known_interfaces...", config.fallback_interface);
                interfaces
                    .iter()
                    .find(|iface| KNOWN_INTERFACES.contains(&iface.name.as_str()))
            })
            .unwrap_or_else(|| {
                // panic if no interface is found
                eprintln!("Error: No interface found");
                process::exit(1);
            })
    } else {
        // try using known_interfaces first
        interfaces
            .iter()
            .find(|iface| KNOWN_INTERFACES.contains(&iface.name.as_str()))
            .or_else(|| {
                // try using fallback_interface if known_interfaces is not found
                println!("Warning: No known interfaces found, trying fallback_interface...");
                interfaces
                    .iter()
                    .find(|iface| iface.name == config.fallback_interface)
            })
            .unwrap_or_else(|| {
                // panic if no interface is found
                eprintln!("Error: No interface found");
                process::exit(1);
            })
    };
    
    println!("Using interface: {}", interface.name);
    
    // get interface network address and cidr
    let network = interface
        .ips
        .iter()
        .find(|ip| ip.is_ipv4())
        .expect("No network address found");

    // get the ip network address
    let ip = network.network();

    // get the cidr
    let cidr = network.prefix();
    
    // create the subnet
    let subnet = IpNetwork::new(ip, cidr).unwrap();

    // store ips in a vector
    let mut ips: Vec<IpAddr> = Vec::new();

    loop {
        for ip in subnet.iter() {
            if connect_to_port(ip, 22) {
                // add the ip to the vector
                ips.push(ip);
            }
        }
        // if there is not more than one ip with open port 22
        if ips.len() == 1 {
            // print the ips
            for ip in ips {
                println!("{}:22 is open", ip);
                let tcp = format!("{}:22", ip);
                let mut session = Session::new().unwrap();
                session.set_tcp_stream(TcpStream::connect(tcp).unwrap());
                session.handshake().unwrap();
                // maybe do connect to all open 22 port and if it connects then do the auth if not then try the next ip
                session.userauth_password(&config.username, &config.password).unwrap();
                let result = run_ssh_command(&mut session, "ls");
                println!("{}", result);
            }
            // exit the program
            process::exit(0);
        } else {
            println!("More than one ip with open port 22");
            process::exit(1);
        }
    }

}