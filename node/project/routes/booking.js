// 예매하기 버튼을 누르면 실행되는 함수
function booking() {
    // 선택한 구단, 좌석, 좌석번호, 요일 및 티켓 수 가져오기
    var selectedTeam = document.getElementById("selectTeam").value;
    var selectedSeat = document.getElementById("selectSeat").value;
    var selectedSeatNum = document.getElementById("selectSeatNum").value;
    var selectedWeekday = document.getElementById("selectWeekday").value;
    var ticketCount = document.getElementById("ticketCount").value;

    // 모든 선택 항목이 선택되었는지 확인
    if (selectedTeam && selectedSeat && selectedSeatNum && selectedWeekday && ticketCount) {
        // 예매 확인 메시지 표시
        alert("예매가 확인되었습니다.");
    } else {
        // 선택되지 않은 경우 알림 메시지 표시
        alert("선택을 확인해주세요.");
    }
}

