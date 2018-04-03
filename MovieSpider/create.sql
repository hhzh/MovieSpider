CREATE TABLE `movie` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '片名',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `aka` varchar(255) DEFAULT NULL COMMENT '又名和译名',
  `origin_url` varchar(255) DEFAULT NULL COMMENT '本电影网址',
  `cover` varchar(255) DEFAULT NULL COMMENT '封面',
  `directors` varchar(255) DEFAULT NULL COMMENT '导演',
  `writers` varchar(255) DEFAULT NULL COMMENT '编剧',
  `actors` varchar(255) DEFAULT NULL COMMENT '主要演员',
  `movie_type` varchar(255) DEFAULT NULL COMMENT '电影类型',
  `rating` varchar(255) DEFAULT NULL COMMENT '评分',
  `officia_website` varchar(255) DEFAULT NULL COMMENT '官网',
  `douban_url` varchar(255) DEFAULT NULL COMMENT '豆瓣地址',
  `intro` text COMMENT '简介',
  `lang` varchar(255) DEFAULT NULL COMMENT '语言',
  `countries` varchar(255) DEFAULT NULL COMMENT '制片国家/地区',
  `year` varchar(255) DEFAULT NULL COMMENT '上映日期',
  `mins` varchar(255) DEFAULT NULL COMMENT '片长',
  `IMDb` varchar(255) DEFAULT NULL COMMENT 'IMDb网址',
  `IMDb_rating` varchar(255) DEFAULT NULL COMMENT 'IMDb评分',
  `awards` text,
  `printscreen` text COMMENT '内容截图',
  `publish_date` varchar(255) DEFAULT NULL COMMENT '发布日期',
  `read_count` varchar(255) DEFAULT NULL COMMENT '点击量',
  `comment_count` varchar(255) DEFAULT NULL COMMENT '评论数',
  `website_url` varchar(255) DEFAULT NULL COMMENT '网站URL',
  `website_name` varchar(255) DEFAULT NULL COMMENT '网站名字',
  `sharpness` varchar(255) DEFAULT NULL COMMENT '清晰度',
  `tags` varchar(255) DEFAULT NULL COMMENT '标签',
  `download_name` varchar(255) DEFAULT NULL COMMENT '下载地址名称',
  `download_url` varchar(255) DEFAULT NULL COMMENT '下载地址',
  `pan_name` varchar(255) DEFAULT NULL COMMENT '百度网盘下载名称',
  `pan_url` varchar(255) DEFAULT NULL COMMENT '网盘下载地址',
  `pan_pwd` varchar(255) DEFAULT NULL COMMENT '网盘密码',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `movie_link` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `moive_id` int(10) DEFAULT NULL COMMENT '电影ID',
  `name` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `sharpness_id` int(3) DEFAULT NULL COMMENT '清晰度ID',
  `sharpness_name` varchar(255) DEFAULT NULL COMMENT '清晰度名称',
  `website_name` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影下载地址';

CREATE TABLE `movie_sharpness` (
  `id` int(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='链接清晰度类型';

