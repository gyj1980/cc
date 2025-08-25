# coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
import re
from urllib.parse import quote

class Spider(Spider):
    def getName(self):
        return "WWGZ影视站"
    
    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass
    
    def isVideoFormat(self, url):
        pass
    
    def manualVideoCheck(self):
        pass
    
    def homeContent(self, filter):
        result = {}
        cateManual = {
            "全部": "1",
            "电影": "1",
            "电视剧": "2", 
            "动漫": "3",
            "综艺": "4",
            "动作片": "5",
            "喜剧片": "6",
            "爱情片": "7",
            "科幻片": "8",
            "恐怖片": "9",
            "剧情片": "10",
            "战争片": "11"
        }
        
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })

        result['class'] = classes
        
        if filter:
            result['filters'] = {
                "1": [
                    {
                        "key": "area",
                        "name": "地区",
                        "value": [
                            {"n": "全部", "v": ""},
                            {"n": "大陆", "v": "大陆"},
                            {"n": "香港", "v": "香港"},
                            {"n": "台湾", "v": "台湾"},
                            {"n": "美国", "v": "美国"},
                            {"n": "韩国", "v": "韩国"},
                            {"n": "日本", "v": "日本"},
                            {"n": "英国", "v": "英国"},
                            {"n": "法国", "v": "法国"},
                            {"n": "印度", "v": "印度"}
                        ]
                    },
                    {
                        "key": "by",
                        "name": "排序",
                        "value": [
                            {"n": "时间", "v": "time"},
                            {"n": "人气", "v": "hits"},
                            {"n": "评分", "v": "score"},
                            {"n": "推荐", "v": "commend"}
                        ]
                    },
                    {
                        "key": "year",
                        "name": "年份",
                        "value": [
                            {"n": "全部", "v": ""},
                            {"n": "2024", "v": "2024"},
                            {"n": "2023", "v": "2023"},
                            {"n": "2022", "v": "2022"},
                            {"n": "2021", "v": "2021"},
                            {"n": "2020", "v": "2020"},
                            {"n": "2019", "v": "2019"},
                            {"n": "2018", "v": "2018"}
                        ]
                    }
                ],
                "2": [
                    {
                        "key": "area",
                        "name": "地区",
                        "value": [
                            {"n": "全部", "v": ""},
                            {"n": "大陆", "v": "大陆"},
                            {"n": "香港", "v": "香港"},
                            {"n": "台湾", "v": "台湾"},
                            {"n": "美国", "v": "美国"},
                            {"n": "韩国", "v": "韩国"},
                            {"n": "日本", "v": "日本"},
                            {"n": "泰国", "v": "泰国"}
                        ]
                    },
                    {
                        "key": "year",
                        "name": "年份",
                        "value": [
                            {"n": "全部", "v": ""},
                            {"n": "2024", "v": "2024"},
                            {"n": "2023", "v": "2023"},
                            {"n": "2022", "v": "2022"},
                            {"n": "2021", "v": "2021"},
                            {"n": "2020", "v": "2020"}
                        ]
                    }
                ]
            }
        return result
    
    def homeVideoContent(self):
        result = {'list': []}
        return result

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        videos = []
        
        area = extend.get('area', '')
        by = extend.get('by', 'time')
        year = extend.get('year', '')
        
        url = f"https://www.wwgz.cn/vod-list-id-{tid}-pg-{pg}-order--by-{by}-class-0-year-{year}-letter--area-{area}-lang-.html"
        
        try:
            rsp = self.fetch(url, headers=self.header)
            html = rsp.text
            
            pattern = r'<li class="col-md-2 col-sm-3 col-xs-4">\s*<a href="([^"]+)" title="([^"]+)"[^>]*>\s*<img[^>]*data-original="([^"]+)"[^>]*>\s*<div class="name">([^<]+)</div>\s*</a>\s*</li>'
            
            matches = re.findall(pattern, html, re.DOTALL)
            
            if not matches:
                pattern2 = r'<li[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>\s*<img[^>]*src="([^"]+)"[^>]*>\s*<h3[^>]*>([^<]+)</h3>'
                matches = re.findall(pattern2, html, re.DOTALL)
                for match in matches:
                    detail_url = match[0]
                    img = match[1]
                    title = match[2]
                    
                    vod_id = re.search(r'/vod-detail-id-(\d+)\.html', detail_url)
                    if vod_id:
                        vod_id = vod_id.group(1)
                    else:
                        vod_id = detail_url
                    
                    videos.append({
                        "vod_id": vod_id,
                        "vod_name": title,
                        "vod_pic": img if img.startswith('http') else f"https://www.wwgz.cn{img}",
                        "vod_remarks": ""
                    })
            else:
                for match in matches:
                    detail_url = match[0]
                    title = match[1]
                    img = match[2]
                    
                    vod_id = re.search(r'/vod-detail-id-(\d+)\..html', detail_url)
                    if vod_id:
                        vod_id = vod_id.group(1)
                    else:
                        vod_id = detail_url
                    
                    videos.append({
                        "vod_id": vod_id,
                        "vod_name": title,
                        "vod_pic": img if img.startswith('http') else f"https://www.wwgz.cn{img}",
                        "vod_remarks": ""
                    })
            
            page_pattern = r'<a[^>]*href="[^"]*pg-(\d+)[^"]*"[^>]*>最后一页</a>'
            page_match = re.search(page_pattern, html)
            if not page_match:
                page_pattern = r'<li><a[^>]*>(\d+)</a></li>\s*</ul>'
                page_match = re.search(page_pattern, html)
            
            if page_match:
                total = int(page_match.group(1))
            else:
                total = 100 if len(videos) > 0 else 1
            
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = total
            result['limit'] = 24
            result['total'] = total * 24
            
        except Exception as e:
            print(f"Error fetching category content: {e}")
            result['list'] = []
            result['page'] = pg
            result['pagecount'] = 1
            result['limit'] = 0
            result['total'] = 0
        
        return result

    def detailContent(self, array):
        result = {'list': []}
        vod_id = array[0]
        
        if vod_id.isdigit():
            url = f"https://www.wwgz.cn/vod-detail-id-{vod_id}.html"
        else:
            url = vod_id
        
        try:
            rsp = self.fetch(url, headers=self.header)
            html = rsp.text
            
            title_pattern = r'<h1[^>]*>([^<]+)</h1>'
            img_pattern = r'<img[^>]*src="([^"]+)"[^>]*alt="[^"]*"[^>]*>'
            year_pattern = r'年份[：:]\s*<a[^>]*>([^<]+)</a>'
            area_pattern = r'地区[：:]\s*<a[^>]*>([^<]+)</a>'
            actor_pattern = r'演员[：:]\s*([^<]*)</div>'
            director_pattern = r'导演[：:]\s*([^<]*)</div>'
            desc_pattern = r'简介[：:]\s*<div[^>]*>([^<]*)</div>'
            
            title = self.regStr(reg=title_pattern, src=html)
            img = self.regStr(reg=img_pattern, src=html)
            year = self.regStr(reg=year_pattern, src=html)
            area = self.regStr(reg=area_pattern, src=html)
            actor = self.regStr(reg=actor_pattern, src=html)
            director = self.regStr(reg=director_pattern, src=html)
            desc = self.regStr(reg=desc_pattern, src=html)
            
            if img and not img.startswith('http'):
                img = f"https://www.wwgz.cn{img}"
            
            play_from = []
            play_url = []
            
            play_sources_pattern = r'<div class="play-source">(.*?)</div>'
            play_sources_match = re.search(play_sources_pattern, html, re.DOTALL)
            
            if not play_sources_match:
                play_sources_pattern = r'<ul class="nav nav-tabs">(.*?)</ul>'
                play_sources_match = re.search(play_sources_pattern, html, re.DOTALL)
            
            if play_sources_match:
                sources_html = play_sources_match.group(1)
                source_pattern = r'<a[^>]*data-id="([^"]*)"[^>]*>([^<]+)</a>'
                sources = re.findall(source_pattern, sources_html)
                
                for source_id, source_name in sources:
                    play_from.append(source_name)
                    
                    play_list_pattern = rf'<div[^>]*data-id="{source_id}"[^>]*>(.*?)</div>'
                    play_list_match = re.search(play_list_pattern, html, re.DOTALL)
                    
                    if play_list_match:
                        play_list_html = play_list_match.group(1)
                        episode_pattern = r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
                        episodes = re.findall(episode_pattern, play_list_html)
                        
                        episode_list = []
                        for ep_url, ep_name in episodes:
                            full_url = ep_url if ep_url.startswith('http') else f"https://www.wwgz.cn{ep_url}"
                            episode_list.append(f"{ep_name}${full_url}")
                        
                        play_url.append("#".join(episode_list))
            
            if not play_from:
                episode_pattern = r'<a[^>]*href="(https?://[^"]*\.m3u8[^"]*)"[^>]*>([^<]*)</a>'
                episodes = re.findall(episode_pattern, html, re.DOTALL)
                if episodes:
                    play_from.append("默认播放源")
                    episode_list = []
                    for ep_url, ep_name in episodes:
                        episode_list.append(f"{ep_name}${ep_url}")
                    play_url.append("#".join(episode_list))
            
            vod = {
                "vod_id": vod_id,
                "vod_name": title or "未知标题",
                "vod_pic": img or "",
                "type_name": "",
                "vod_year": year or "",
                "vod_area": area or "",
                "vod_remarks": "",
                "vod_actor": actor or "",
                "vod_director": director or "",
                "vod_content": desc or "",
                "vod_play_from": "$$$".join(play_from) if play_from else "默认播放源",
                "vod_play_url": "$$$".join(play_url) if play_url else ""
            }
            
            result['list'] = [vod]
            
        except Exception as e:
            print(f"Error fetching detail content: {e}")
            import traceback
            traceback.print_exc()
        
        return result

    def searchContent(self, key, quick):
        result = {'list': []}
        try:
            search_url = f"https://www.wwgz.cn/vod-search-pg-1-wd-{quote(key)}.html"
            rsp = self.fetch(search_url, headers=self.header)
            html = rsp.text
            
            pattern = r'<li class="col-md-2 col-sm-3 col-xs-4">\s*<a href="([^"]+)" title="([^"]+)"[^>]*>\s*<img[^>]*data-original="([^"]+)"[^>]*>\s*<div class="name">([^<]+)</div>\s*</a>\s*</li>'
            
            matches = re.findall(pattern, html, re.DOTALL)
            
            for match in matches:
                detail_url = match[0]
                title = match[1]
                img = match[2]
                
                vod_id = re.search(r'/vod-detail-id-(\d+)\..html', detail_url)
                if vod_id:
                    vod_id = vod_id.group(1)
                else:
                    vod_id = detail_url
                
                result['list'].append({
                    "vod_id": vod_id,
                    "vod_name": title,
                    "vod_pic": img if img.startswith('http') else f"https://www.wwgz.cn{img}",
                    "vod_remarks": ""
                })
                
        except Exception as e:
            print(f"Error searching: {e}")
            
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        
        if id.endswith('.m3u8') or id.endswith('.mp4'):
            result["parse"] = 0
            result["playUrl"] = ''
            result["url"] = id
        else:
            try:
                rsp = self.fetch(id, headers=self.header)
                html = rsp.text
                
                m3u8_pattern = r'"(https?://[^"]*\.m3u8[^"]*)"'
                m3u8_match = re.search(m3u8_pattern, html)
                
                if m3u8_match:
                    result["parse"] = 0
                    result["playUrl"] = ''
                    result["url"] = m3u8_match.group(1)
                else:
                    result["parse"] = 1
                    result["playUrl"] = ''
                    result["url"] = id
            except:
                result["parse"] = 1
                result["playUrl"] = ''
                result["url"] = id
        
        result["header"] = self.header
        
        return result

    def regStr(self, reg, src):
        try:
            pattern = re.compile(reg, re.DOTALL)
            match = pattern.search(src)
            if match:
                return match.group(1).strip()
        except:
            pass
        return ""

    def localProxy(self, param):
        action = {
            'url': '',
            'header': '',
            'param': '',
            'type': 'string'
        }
        return [200, "video/MP2T", action, ""]

    config = {
        "player": {},
        "filter": {}
    }
    
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.wwgz.cn/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }