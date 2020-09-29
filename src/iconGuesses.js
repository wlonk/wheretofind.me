function parseUrl(url) {
  const a = document.createElement('a');
  a.href = url;
  return a;
}

const iconGuesses = [
  { fn: () => true, val: 'fas fa-link' },
  {
    fn: url => parseUrl(url).hostname.endsWith('500px.com'),
    val: 'fab fa-500px',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('angel.co'),
    val: 'fab fa-angellist',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('bandcamp.com'),
    val: 'fab fa-bandcamp',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('behance.net'),
    val: 'fab fa-behance',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('blogger.com'),
    val: 'fab fa-blogger-b',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('blogspot.com'),
    val: 'fab fa-blogger-b',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('bitbucket.org'),
    val: 'fab fa-bitbucket',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('codepen.io'),
    val: 'fab fa-codepen',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('dailymotion.com'),
    val: 'fab fa-dailymotion',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('dev.to'),
    val: 'fab fa-dev',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('deviantart.com'),
    val: 'fab fa-deviantart',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('discordapp.com'),
    val: 'fab fa-discord',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('dribbble.com'),
    val: 'fab fa-dribbble',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('drive.google.com'),
    val: 'fab fa-google-drive',
  },
  { fn: url => parseUrl(url).hostname.endsWith('ello.co'), val: 'fab fa-ello' },
  {
    fn: url => parseUrl(url).hostname.endsWith('etsy.com'),
    val: 'fab fa-etsy',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('facebook.com'),
    val: 'fab fa-facebook',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('figma.com'),
    val: 'fab fa-figma',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('flickr.com'),
    val: 'fab fa-flickr',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('flipboard.com'),
    val: 'fab fa-flipboard',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('foursquare.com'),
    val: 'fab fa-foursquare',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('github.com'),
    val: 'fab fa-github',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('gitlab.com'),
    val: 'fab fa-gitlab',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('goodreads.com'),
    val: 'fab fa-goodreads',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('hackerrank.com'),
    val: 'fab fa-hackerrank',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('instagram.com'),
    val: 'fab fa-instagram',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('itch.io'),
    val: 'fab fa-itch-io',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('jsfiddle.net'),
    val: 'fab fa-jsfiddle',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('kaggle.com'),
    val: 'fab fa-kaggle',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('keybase.io'),
    val: 'fab fa-keybase',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('kickstarter.com'),
    val: 'fab fa-kickstarter',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('last.fm'),
    val: 'fab fa-lastfm',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('leanpub.com'),
    val: 'fab fa-leanpub',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('linkedin.com'),
    val: 'fa fa-linkedin',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('matrix.to'),
    val: 'fa fa-matrix-org',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('medium.com'),
    val: 'fab fa-medium',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('news.ycombinator.com'),
    val: 'fab fa-hacker-news-square',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('npmjs.com'),
    val: 'fab fa-npm',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('patreon.com'),
    val: 'fab fa-patreon',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('periscope.tv'),
    val: 'fab fa-periscope',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('pinterest.com'),
    val: 'fab fa-pinterest',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('producthunt.com'),
    val: 'fab fa-product-hunt',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('play.google.com'),
    val: 'fab fa-google-play',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('plus.google.com'),
    val: 'fab fa-google-plus-g',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('quora.com'),
    val: 'fab fa-quora',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('ravelry.com'),
    val: 'fab fa-ravelry',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('reddit.com'),
    val: 'fab fa-reddit',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('skype.com'),
    val: 'fab fa-skype',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('slack.com'),
    val: 'fab fa-slack',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('slideshare.net'),
    val: 'fab fa-slideshare',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('snapchat.com'),
    val: 'fab fa-snapchat-ghost',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('soundcloud.com'),
    val: 'fab fa-soundcloud',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('spotify.com'),
    val: 'fab fa-spotify',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('speakerdeck.com'),
    val: 'fab fa-speakerdeck',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('stackexchange.com'),
    val: 'fab fa-stack-exchange',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('stackoverflow.com'),
    val: 'fab fa-stack-overflow',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('steamcommunity.com'),
    val: 'fab fa-steam',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('strava.com'),
    val: 'fab fa-strava',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('t.me'),
    val: 'fab fa-telegram-plane',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('teamspeak.com'),
    val: 'fab fa-teamspeak',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('tiktok.com'),
    val: 'fab fa-tiktok',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('trello.com'),
    val: 'fab fa-trello',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('tripadvisor.com'),
    val: 'fab fa-tripadvisor',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('tumblr.com'),
    val: 'fab fa-tumblr',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('twitch.tv'),
    val: 'fab fa-twitch',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('twitter.com'),
    val: 'fab fa-twitter',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('unsplash.com'),
    val: 'fab fa-unsplash',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('untappd.com'),
    val: 'fab fa-untappd',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('vimeo.com'),
    val: 'fab fa-vimeo',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('vk.com'),
    val: 'fab fa-vk',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('wikipedia.org'),
    val: 'fab fa-wikipedia-w',
  },
  {
    fn: url => parseUrl(url).hostname.endsWith('youtube.com'),
    val: 'fab fa-youtube',
  },

  {
    fn: url => parseUrl(url).hostname.includes('paypal'),
    val: 'fab fa-paypal',
  },
  {
    fn: url => parseUrl(url).hostname.includes('pixelfed'),
    val: 'fa fa-pixelfed',
  },
  {
    fn: url => parseUrl(url).hostname.includes('pora'),
    val: 'fab fa-diaspora',
  },
  {
    fn: url => parseUrl(url).hostname.includes('mastodon'),
    val: 'fab fa-mastodon',
  },
  {
    fn: url => parseUrl(url).hostname.includes('telegram'),
    val: 'fab fa-telegram-plane',
  },
  {
    fn: url => parseUrl(url).hostname.includes('wordpress'),
    val: 'fab fa-wordpress-simple',
  },

  { fn: url => parseUrl(url).protocol === 'mailto:', val: 'fas fa-envelope' },
];

export default iconGuesses;
