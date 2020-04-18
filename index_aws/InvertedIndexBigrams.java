import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class InvertedIndexBigrams {

    public static class TokenizerMapper extends Mapper<Object, Text, Text, Text>{

        private Text docId = new Text();
        private Text word = new Text();

        public void map(Object key, Text value, Context context
        ) throws IOException, InterruptedException {
            // To get current document ID
            StringTokenizer itr = new StringTokenizer(value.toString());
            docId.set(itr.nextToken());
            //initialize content: replace special characters and numerials and space
            //convert all the words to the lowercase
            String content = value.toString().replaceAll("[^a-zA-Z]", " ")
                    .toLowerCase();
            StringTokenizer iter = new StringTokenizer(content);
            //generate bigrams
            String first = iter.nextToken();
            String second = iter.nextToken();
            while (iter.hasMoreTokens()) {
                String bigrams = first + " " + second;
                word.set(bigrams);
                context.write(word, docId);
                first = second;
                second = iter.nextToken();
            }
        }
    }

    public static class InvertedReducer extends Reducer<Text,Text,Text,Text> {

        public void reduce(Text key, Iterable<Text> values,
                           Context context
        ) throws IOException, InterruptedException {

            Map<String,Integer> docMap = new HashMap<>();
            //store word frequency in the file
            for(Text val : values){
                String word = val.toString();
                docMap.put(word, (int)docMap.getOrDefault(word, 0) + 1);
            }

            //create a string to store docID:filefreq
            StringBuilder docList = new StringBuilder();
            for(Object docID : docMap.keySet()){
                docList.append(docID.toString() + ":" + docMap.get(docID.toString()) + "\t");
            }
            docList.deleteCharAt(docList.length()-1);//delete last space
            context.write(key, new Text(docList.toString()));
        }
    }

    public static void main(String[] args) throws Exception {

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Inverted Index");
        job.setJarByClass(InvertedIndexBigrams.class);
        job.setMapperClass(TokenizerMapper.class);

        job.setReducerClass(InvertedReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }


}