<?php

class MovieService
{
    const CURRENT_USER_ID = 1;
    public static function searchMotor($query){
        $url = API_BASE_URL . "/search?q=" . urlencode($query);
        $response = file_get_contents($url, true);
        return $response;
    }

    public static function getWatchlist($user_id)
    {
        $url = API_BASE_URL . "/watchlist" . "/" . $user_id;
        $response = file_get_contents($url);
        return json_decode($response, true);
    }

    public static function addWatchlist($metadata,$user_id){
        $url = API_BASE_URL . "/watchlist";
        
        $data = json_decode($metadata,true);
        $data['user_id'] = $user_id;
        $content = json_encode($data);

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

    public static function creerCompte($data){
        $url = API_BASE_URL . "/compte";
        $content = json_encode($data);
        $options = [
            "http" => [
                "method" => "POST",
                "header" => "Content-Type: application/json", 
                "content" => $content,
                "ignore_errors" => true
            ]
        ];
        $context = stream_context_create($options);
        $response = file_get_contents($url, false, $context);
        return json_decode($response,true);
    }

    public static function connexion($data){
        $url = API_BASE_URL . "/connexion";
        $content = json_encode($data);
        $options = [
            "http" => [
                "method" => "POST",
                "header" => "Content-Type: application/json", 
                "content" => $content,
                "ignore_errors" => true
            ]
        ];
        $context = stream_context_create($options);
        $response = file_get_contents($url, false, $context);
        return json_decode($response,true);
    }

    public static function updateProfile($data){
        $url = API_BASE_URL . "/compte" . "/" . $data["id"];
        $content = json_encode($data);
        $options = [
            "http" => [
                "method" => "PUT",
                "header" => "Content-Type: application/json", 
                "content" => $content,
                "ignore_errors" => true
            ]
        ];
        $context = stream_context_create($options);
        $response = file_get_contents($url,false,$context);
        return json_decode($response,true);
    }

    public static function deleteProfile($id_user){
        $url = API_BASE_URL . "/compte" . "/" . $id_user;
        $options = [
            "http" => [
                "method" => "DELETE",
                "header" => "Content-Type: application/json", 
                "ignore_errors" => true
            ]
        ];
        $context = stream_context_create($options);
        $response = file_get_contents($url,false,$context);
        return json_decode($response,true);
    }
}
?>