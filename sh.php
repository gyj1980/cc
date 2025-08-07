<?php
//https://summer.bestv.cn/smg_gongzhonghao_h5/#/home
//http://kaniptv.com
$id = $_GET['id'];
$url = "https://bp-api.bestv.cn/cms/api/live/channels";
$options = [
    "http" => [
        "header"  => "Content-Type: application/json\r\n",
        "method"  => "POST",
        "content" => '{}',
        "ignore_errors" => true
    ]
];
$response = file_get_contents($url, false, stream_context_create($options));
if ($response) {
    $data = json_decode($response, true);
    foreach ($data['dt'] ?? [] as $channel) {
        if (($channel['id'] ?? '') == $id && !empty($channel['channelUrl'])) {
            header('Location: ' . $channel['channelUrl']);
            exit;
        }
    }
}
?>