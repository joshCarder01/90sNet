usage() {
    echo "Usage: $0 [-r] [-s] [-h]"
    echo -e "\t-r\tGenerate random data for database"
    echo -e "\t-s\tGenerate seeded test data"
}

while getopts "rsh" o; do
    case "${o}" in
        r)
            COMMAND="random"
            ;;
        s)
            COMMAND="seed"
            ;;
        h|*)
            usage
            ;;
    esac
done
shift $((OPTIND-1))


docker-compose build
docker-compose run flask_app flask db ${COMMAND:=init}

