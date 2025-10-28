const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
const scrollTopBtn = document.querySelector('.scroll-top');
const tabs = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.tab-panel');
const accordionTriggers = document.querySelectorAll('.accordion__trigger');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        const expanded = navToggle.getAttribute('aria-expanded') === 'true';
        navToggle.setAttribute('aria-expanded', String(!expanded));
        navLinks.classList.toggle('open');
    });

    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navToggle.setAttribute('aria-expanded', 'false');
            navLinks.classList.remove('open');
        });
    });
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', event => {
        const targetId = anchor.getAttribute('href');
        const target = document.querySelector(targetId);
        if (target) {
            event.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

const setActiveTab = tab => {
    tabs.forEach(btn => btn.classList.toggle('active', btn === tab));
    panels.forEach(panel => panel.classList.toggle('active', `panel-${tab.dataset.tab}` === panel.id));
    tabs.forEach(btn => btn.setAttribute('aria-selected', btn === tab ? 'true' : 'false'));
};

tabs.forEach(tab => {
    tab.addEventListener('click', () => setActiveTab(tab));
    tab.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            setActiveTab(tab);
        }
    });
});

accordionTriggers.forEach(trigger => {
    const panel = trigger.nextElementSibling;
    trigger.addEventListener('click', () => {
        const expanded = trigger.getAttribute('aria-expanded') === 'true';
        trigger.setAttribute('aria-expanded', String(!expanded));
        panel.classList.toggle('open');
    });
});

if (scrollTopBtn) {
    const onScroll = () => {
        if (window.scrollY > 300) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    };

    window.addEventListener('scroll', onScroll);
    onScroll();

    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
