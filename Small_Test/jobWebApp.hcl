job "Web" {

    group "WebApplication" {

        network {
            port "web" {
                static="8080"
            }
        }

        service {
            name      = "test-web-svc"
            port      = "web"
            provider  = "nomad"
        }

        task "FlaskApp" {
            driver = "docker"

            # Should change to whatever is hosting the docker images
            artifact {
                source = "http://0.0.0.0:9900/web_app_image.tar"
                options {
                    archive = false
                }
            }

            config {
                load = "web_app_image.tar"
                image = "web-app:local"
                ports = ["web"]
            }



        }
    }
}