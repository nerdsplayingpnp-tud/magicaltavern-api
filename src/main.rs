use actix_web::{get, web, App, HttpServer, Responder};
use clap::Parser;

/// magicaltavern API Server.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long, default_value_t = 8080)]
    port: u16,

    /// Number of web workers to spawn. Defaults to the number of CPUs available.
    #[arg(short, long, default_value_t = num_cpus::get() as u16)]
    workers: u16,
}

#[get("/")]
async fn index() -> impl Responder {
    "Hello, World!"
}

#[get("/{name}")]
async fn hello(name: web::Path<String>) -> impl Responder {
    format!("Hello {}!", &name)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let args = Args::parse();
    println!(
        "Starting magicaltavern-api with {} workers on port {}",
        args.workers, args.port
    );
    HttpServer::new(|| App::new().service(index).service(hello))
        .workers(args.workers as usize)
        .bind(("127.0.0.1", args.port))?
        .run()
        .await
}
