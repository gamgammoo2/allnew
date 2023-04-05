#!/usr/bin/ruby

require 'rbygem'
require 'mongo'

$client = Mongo::Client.new(['0.0.0.0:27017'],
    :database => 'test')  ##로켓대쉬라고 칭함 => ##몽고랑 루비 연결(루비는 설치 방금 했었음)
Mongo::Logger.logger.level = ::Logger::ERROR
$users = $client[:users]
puts 'connected!'
