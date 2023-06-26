document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var today = new Date();

  var calendar = new FullCalendar.Calendar(calendarEl, {
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,list'
    },
    initialDate: today,
    navLinks: true, // can click day/week names to navigate views
    selectable: true,
    selectMirror: true,
    select: function(arg) {
      console.log('clicked')
      var modal = document.getElementById('eventModal')
      modal.style.display = 'block'
      calendar.unselect()
    },
   
    eventClick: function(arg) {
      if (confirm('Are you sure you want to delete this event?')) {
        arg.event.remove()
      }
    },
    editable: true,
    dayMaxEvents: true, // allow "more" link when too many events
  });

  calendar.render();
});
const closeBtn1 = document.getElementById('modalClose1');
const closeBtn2 = document.getElementById('modalClose2');
closeBtn1.addEventListener('click',()=>{
  const eventModal = document.getElementById('eventModal')
  eventModal.style.display = 'none';
});
closeBtn2.addEventListener('click',()=>{
  const eventModal = document.getElementById('eventModal')
  eventModal.style.display = 'none';
});