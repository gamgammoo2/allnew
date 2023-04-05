#!/usr/bin/ruby

require 'rbygem'
require 'mongo'

$client = Mongo::Client.new(['0.0.0.0:27017'],:database => 'ruby')  ##로켓대쉬라고 칭함 => ##몽고랑 루비 연결(루비는 설치 방금 했었음)
Mongo::Logger.logger.level = ::Logger::ERROR
$emp = $client[:emp]
puts 'connected!'

cursor = $emp.find()
cursor.each do | doc |
    puts doc
end