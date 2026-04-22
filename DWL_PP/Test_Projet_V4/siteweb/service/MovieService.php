<?php

class MovieService
{
    public static function searchMotor($query){
        $url = API_BASE_URL . "/search?q=" . urlencode($query);
        $response = file_get_contents($url, true);
        return $response;
    }

    public static function getWatchlist()
    {
        $url = API_BASE_URL . "/watchlist";
        $response = file_get_contents($url);
        return json_decode($response, true);
    }

    public static function addWatchlist($metadata){
        $url = API_BASE_URL . "/watchlist";
        $content = $metadata;
        $options = [
            "http" => [
                "method" => "POST",
                "header" => "Content-Type: application/json",
                "content" => $content
            ]
        ];
        $context = stream_context_create($options);
        $response = file_get_contents($url, false, $context);

        return $response;

    }
    public static function getMovieData($filmID){
        $url = API_BASE_URL . "/movies"  . "/" . $filmID;
        $response = file_get_contents($url, true);
        return $response;
    }
}
?>