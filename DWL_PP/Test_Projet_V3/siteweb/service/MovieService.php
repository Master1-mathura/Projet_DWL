<?php

class MovieService
{
    
    public static function searchMotor($query){
        $url = API_BASE_URL . "/search";
        $content = json_encode($query);

        //https://www.geeksforgeeks.org/php/how-to-send-a-post-request-with-php/

        //$options : C'est un tableau de configuration pour la requête HTTP.
        // - 'method' => 'POST' : On précise qu'on veut faire un POST ( par défaut, file_get_contents fait un GET).
        // - 'header' => 'Content-Type: application/json' : Ici on indique que le contenu qu'on envoie est du JSON
        // L'API Flask, elle, attend request.get_json(). Donc si on n'envoie pas ce header, Flask ne pourra pas lire les données correctement.
        // - 'content' => $content : C'est les données du nouvel étudiant encodées en JSON.
        
        //Pourquoi http : 
            //stream_context_create() fonctionne avec des protocoles différents, pas seulement HTTP.
            //En mettant 'http', on indique que ces options sont pour les requêtes HTTP. 

        $options = [
            "http" => [
                "method" => "GET",
                "header" => "Content-Type: application/json", 
                "content" => $content
            ]
        ];


        //On cree un contexte de flux (stream context) avec ces options.
        //Parce que file_get_contents() ne peut pas faire directement du POST avec JSON
        //mais si on lui donne ce contexte, il sait comment envoyer la requête correctement.
        $context = stream_context_create($options); 
        
        //Là on fais vraiment la requête HTTP
        //$url -> c'est l'URL de ton API Flask
        //false -> inutile ici, juste pour dire pas d'inclusion de fichiers
        // $context -> la configuraition qu'on vint de creer, qui indique ce c'est un POST et que c'est du JSON
        
        $response = file_get_contents($url, false, $context);

        return $response;
    }
}
?>