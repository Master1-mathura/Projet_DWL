<?php

class MovieService
{


    public static function getAll()
    {
        $url = API_BASE_URL . "/total_watchlist";
        $response = file_get_contents($url);
        return json_decode($response, true);
    }

    public static function getMovieData($filmID){
        $url = API_BASE_URL . "/get_metadata";
        $content = json_encode(["film_ID" => $filmID]);
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

    public static function addWatchlist($metadata){
        $url = API_BASE_URL . "/ajout_watchlist";
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
    public static function searchMotor($query){
        $url = API_BASE_URL . "/search";
        $data_to_send = ["query" => $query];
        $content = json_encode($data_to_send);
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
}
?>