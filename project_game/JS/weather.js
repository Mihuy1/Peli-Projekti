// api here

async function getWeatherData(lat, lon) {
    try {
        const query = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${api}&units=metric`;

        const response = await fetch(query);

        const jsonData = await response.json();

        console.log(jsonData["weather"][0]["description"]);

        return jsonData;
    }

    catch(error) {
        console.log(`weather fetch encountered an error: ${error}`);
    }

    finally {
        console.log('Weather fetch complete');
    }
}

// Helsinki lat: 60.199983, lon: 24.959373

const helsinki_lat= 60.199983;
const helsinki_lon = 24.959373;

getWeatherData(helsinki_lat, helsinki_lon)
    .then((data) => {
        console.log(data);
    })
    .catch((error) => {
        console.log(`An error occurred: ${error}`);
    });

