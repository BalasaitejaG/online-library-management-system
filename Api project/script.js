document.addEventListener("DOMContentLoaded", () => {
  const cityInput = document.getElementById("city-input");
  const GetWeatherBtn = document.getElementById("get-weather-btn");
  const WeatherInfo = document.getElementById("weather-info");
  const CityName = document.getElementById("city-name");
  const Temperature = document.getElementById("temperature");
  const Description = document.getElementById("description");
  const ErrorMsg = document.getElementById("error-message");
  const API_KEY = "9a916593c52d3bd047712e52fa55e216";

  //button
  GetWeatherBtn.addEventListener("click", async () => {
    const city = cityInput.value.trim();
    if (!city) return;

    // it may throw an error
    // server/database is always in another continent

    try {
      const weatherData = await FetchWeather(city);
      displayWeatherData(weatherData);
    } catch (error) {
      showError();
    }
  });

  async function FetchWeather(city) {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${API_KEY}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(" City Not found");
    }
    const data = await response.json();
    return data;
  }

  function displayWeatherData(data) {
    console.log(data);
    const { name, main, weather } = data;
    CityName.textContent = name;
    Temperature.textContent = `Temperature : ${main.temp}`;
    Description.textContent = `Weather : ${weather[0].description}`;
    WeatherInfo.classList.remove("hidden");
    ErrorMsg.classList.add("hidden");
  }

  function DisplayError() {
    WeatherInfo.classList.remove("hidden");
    ErrorMsg.classList.add("hidden");
  }
});
