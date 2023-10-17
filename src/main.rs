use std::fmt::Display;

use actix_web::{get, App, HttpServer, Responder};
use clap::{Parser, ValueEnum};

#[derive(Parser, Debug, Clone, Copy)]
enum DatabaseType {
    SQLite,
    Postgres,
    MySQL,
}

impl Display for DatabaseType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DatabaseType::SQLite => write!(f, "sqlite"),
            DatabaseType::Postgres => write!(f, "postgres"),
            DatabaseType::MySQL => write!(f, "mysql"),
        }
    }
}

impl ValueEnum for DatabaseType {
    fn value_variants<'a>() -> &'a [Self] {
        &[Self::SQLite, Self::Postgres, Self::MySQL]
    }

    fn to_possible_value(&self) -> Option<clap::builder::PossibleValue> {
        match self {
            DatabaseType::SQLite => Some(clap::builder::PossibleValue::new("sqlite")),
            DatabaseType::Postgres => Some(clap::builder::PossibleValue::new("postgres")),
            DatabaseType::MySQL => Some(clap::builder::PossibleValue::new("mysql")),
        }
    }
}

/// magicaltavern API Server.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long, default_value_t = 8080)]
    port: u16,

    /// Number of web workers to spawn. Defaults to the number of CPUs available.
    #[arg(short, long, default_value_t = num_cpus::get() as u16)]
    workers: u16,

    #[arg(short = 'u', long)]
    database_url: Option<String>,

    #[arg(short, long, default_value_t = DatabaseType::SQLite)]
    database_type: DatabaseType,
}

#[get("/api/v3")]
async fn hello() -> impl Responder {
    "The API is running!"
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let args = Args::parse();
    println!(
        "Starting magicaltavern-api with {} workers on port {}",
        args.workers, args.port
    );
    HttpServer::new(|| App::new().service(hello))
        .workers(args.workers as usize)
        .bind(("127.0.0.1", args.port))?
        .run()
        .await
}
